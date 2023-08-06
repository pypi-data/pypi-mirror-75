#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#

import uuid
import json
import logging

from v_bootstrap.onboard.config import Config

from v_bootstrap.onboard.board_base import BoardBase
from v_bootstrap.utils.errors import BoardError
from v_bootstrap.utils.connectors import SSHConnector
logger = logging.getLogger(__name__)


class BoardVirtual(BoardBase):
    PATH_HW_ID = '/etc/guid'
    OLD_PATH_SM_CERTS = '/var/aos/servicemanager/data/fcrypt'
    OLD_PATH_VIS_CFG = '/var/aos/vis/visconfig.json'
    OLD_PATH_UM_CFG = '/var/aos/updatemanager/aos_updatemanager.cfg'
    PATH_SERVICE_MANAGER_CFG = '/var/aos/servicemanager/aos_servicemanager.cfg'

    CONFIGS_FOLDER = '/etc/aos/'
    CERTIFICATES_FOLDER = '/var/aos/crts/'

    SERVICE_MANAGER_CONFIG_FILENAME = 'aos_servicemanager.cfg'
    UPDATE_MANAGER_CONFIG_FILENAME = 'aos_updatemanager.cfg'
    VIS_CONFIG_FILENAME_1 = 'visconfig.json'
    VIS_CONFIG_FILENAME_2 = 'aos_vis.cfg'
    MODEL_FILE_NAME = 'model_name.txt'
    HW_ID_FILE_NAME = 'hardware_id.txt'

    def __init__(self, address, port=22, cred=None):
        super(BoardVirtual, self).__init__()
        self._address = address
        self._port = port
        self._cred = cred

    def init_connector(self):
        ssh = SSHConnector(self._address, self._port, self._cred)
        ssh.connect()

        return ssh

    def _generate_pair(self, p_type):
        update_config = self.read_file(self.CONFIGS_FOLDER + self.UPDATE_MANAGER_CONFIG_FILENAME)
        board_config = Config()
        # Detecting where to place certificates
        update_config = self.read_file(self.CONFIGS_FOLDER + self.UPDATE_MANAGER_CONFIG_FILENAME)

        if not update_config:
            update_config = self.read_file(self.OLD_PATH_UM_CFG)

        if not update_config:
            raise BoardError("Can't find Update Manager Config.")

        try:
            config = json.loads(update_config)
        except ValueError as e:
            logger.debug(e)
            raise BoardError("Failed to load update manager configuration.")

        board_config.online_key_folder = BoardVirtual.OLD_PATH_SM_CERTS
        board_config.online_key_filename = 'vehicle_offline.key.pem'
        board_config.online_cert_folder = BoardVirtual.OLD_PATH_SM_CERTS
        board_config.online_cert_filename = 'vehicle_offline.crt.pem'
        board_config.offline_key_folder = BoardVirtual.OLD_PATH_SM_CERTS
        board_config.offline_key_filename = 'vehicle_online.key.pem'
        board_config.offline_cert_folder = BoardVirtual.OLD_PATH_SM_CERTS
        board_config.offline_cert_filename = 'vehicle_online.crt.pem'

        crt_config = config.get("CrtModules", [])
        for item in crt_config:
            cert_folder = item.get("Params", {}).get("StoragePath")
            old_name_style = False
            if cert_folder and item.get("ID"):
                if item.get("ID") == 'online':
                    board_config.online_key_folder = cert_folder
                    board_config.online_key_filename = 'unit_offline.pem.key'
                    board_config.online_cert_folder = cert_folder
                    board_config.online_cert_filename = 'unit_offline.pem.crt'
                elif item.get("ID") == 'offline':
                    board_config.offline_key_folder = cert_folder
                    board_config.offline_key_filename = 'unit_online.pem.key'
                    board_config.offline_cert_folder = cert_folder
                    board_config.offline_cert_filename = 'unit_online.pem.crt'

        self._create_dir(board_config.online_key_folder)
        self._create_dir(board_config.online_cert_folder)
        self._create_dir(board_config.offline_key_folder)
        self._create_dir(board_config.offline_cert_folder)

        if not board_config.online_key_folder.endswith("/"):
            board_config.online_key_folder = board_config.online_key_folder + '/'

        if not board_config.online_cert_folder.endswith("/"):
            board_config.online_cert_folder = board_config.online_cert_folder + '/'

        if not board_config.offline_key_folder.endswith("/"):
            board_config.offline_key_folder = board_config.offline_key_folder + '/'

        if not board_config.offline_cert_folder.endswith("/"):
            board_config.offline_cert_folder = board_config.offline_cert_folder + '/'

        if p_type == 'online':
            pkeys_prefix = board_config.online_key_folder + board_config.online_key_filename
        elif p_type == 'offline':
            pkeys_prefix = board_config.offline_key_folder + board_config.offline_key_filename

        # generate private
        cmd = "openssl genrsa -out {} {}".format(pkeys_prefix, 2048)
        resp = self.connector.execute(cmd)
        if resp.exit_code:
            logger.error('Failed to generate key.')
            raise BoardError("Failed to generate key.")

        # generate public
        public_name = '.'.join((pkeys_prefix, 'pub'))
        cmd = "openssl rsa -in {} -outform " \
              "PEM -pubout -out {}".format(pkeys_prefix, public_name)
        resp = self.connector.execute(cmd)
        if resp.exit_code:
            logger.error('Failed to generate public key.')
            raise BoardError("Failed to generate public key.")

        cmd = "cat {}".format(public_name)
        pub_key = self.connector.execute(cmd).data

        return pub_key

    def _create_dir(self, dir_path):
        cmd = "mkdir -p {}".format(dir_path)
        resp = self.connector.execute(cmd)
        if resp.exit_code:
            logger.error("Failed to create dir %s", dir_path)
            raise BoardError("Failed to create dir %s", dir_path)

    def _delete_dir(self, dir_path):
        cmd = "rm -r {}".format(dir_path)
        resp = self.connector.execute(cmd)
        if resp.exit_code:
            logger.error("Failed to delete dir %s", dir_path)
            raise BoardError("Failed to delete dir %s", dir_path)

    def _set_certificates(self, online_cert_cont, offline_cert_cont, board_config):
        """ Saves certificates on board. """
        # Detecting where to place certificates
        update_config = self.read_file(self.CONFIGS_FOLDER + self.UPDATE_MANAGER_CONFIG_FILENAME)

        if not update_config:
            update_config = self.read_file(self.OLD_PATH_UM_CFG)

        if not update_config:
            raise BoardError("Can't find Update Manager Config.")

        try:
            config = json.loads(update_config)
        except ValueError as e:
            logger.debug(e)
            raise BoardError("Failed to load update manager configuration.")

        board_config.online_key_folder = BoardVirtual.OLD_PATH_SM_CERTS
        board_config.online_key_filename = 'vehicle_offline.key.pem'
        board_config.online_cert_folder = BoardVirtual.OLD_PATH_SM_CERTS
        board_config.online_cert_filename = 'vehicle_offline.crt.pem'
        board_config.offline_key_folder = BoardVirtual.OLD_PATH_SM_CERTS
        board_config.offline_key_filename = 'vehicle_online.key.pem'
        board_config.offline_cert_folder = BoardVirtual.OLD_PATH_SM_CERTS
        board_config.offline_cert_filename = 'vehicle_online.crt.pem'

        crt_config = config.get("CrtModules", [])
        for item in crt_config:
            cert_folder = item.get("Params", {}).get("StoragePath")
            old_name_style = False
            if cert_folder and item.get("ID"):
                if item.get("ID") == 'online':
                    board_config.online_key_folder = cert_folder
                    board_config.online_key_filename = 'unit_offline.pem.key'
                    board_config.online_cert_folder = cert_folder
                    board_config.online_cert_filename = 'unit_offline.pem.crt'
                elif item.get("ID") == 'offline':
                    board_config.offline_key_folder = cert_folder
                    board_config.offline_key_filename = 'unit_online.pem.key'
                    board_config.offline_cert_folder = cert_folder
                    board_config.offline_cert_filename = 'unit_online.pem.crt'

        self._create_dir(board_config.online_key_folder)
        self._create_dir(board_config.online_cert_folder)
        self._create_dir(board_config.offline_key_folder)
        self._create_dir(board_config.offline_cert_folder)

        if not board_config.online_key_folder.endswith("/"):
            board_config.online_key_folder = board_config.online_key_folder + '/'

        if not board_config.online_cert_folder.endswith("/"):
            board_config.online_cert_folder = board_config.online_cert_folder + '/'

        if not board_config.offline_key_folder.endswith("/"):
            board_config.offline_key_folder = board_config.offline_key_folder + '/'

        if not board_config.offline_cert_folder.endswith("/"):
            board_config.offline_cert_folder = board_config.offline_cert_folder + '/'

        self.write_to_file(
            board_config.offline_cert_folder + board_config.offline_cert_filename,
            offline_cert_cont
        )
        self.write_to_file(
            board_config.online_cert_folder + board_config.online_cert_filename,
            online_cert_cont
        )

    _STORAGE_ADAPTER = 'storageadapter'
    _KEY_VIN = 'Attribute.Vehicle.VehicleIdentification.VIN'
    _KEY_CLAIM = 'Attribute.Vehicle.UserIdentification.Users'

    def _update_vis_config(self, vin, claim):
        logger.debug("Updating VIS configuration ...")

        vis_file_name = self.CONFIGS_FOLDER + self.VIS_CONFIG_FILENAME_2
        if not self.is_file_exist(vis_file_name):
            vis_file_name = self.CONFIGS_FOLDER + self.VIS_CONFIG_FILENAME_1
            if not self.is_file_exist(vis_file_name):
                vis_file_name = self.OLD_PATH_VIS_CFG

        ret = self.read_file(vis_file_name)

        try:
            config = json.loads(ret)
        except ValueError as e:
            logger.debug(e)
            raise BoardError("Failed to set VIS configuration.")

        try:
            for pos, a in enumerate(config['Adapters']):
                if BoardVirtual._STORAGE_ADAPTER in a['Plugin']:
                    data = a['Params']['Data']
                    data[BoardVirtual._KEY_VIN]['Value'] = vin
                    data[BoardVirtual._KEY_CLAIM]['Value'] = [claim]
        except KeyError as e:
            logger.debug(e)
            raise BoardError("Failed to set VIS configuration")

        vis_cfg = json.dumps(config, indent=4)
        self.write_to_file(vis_file_name, vis_cfg)

    def _update_service_manager_config(self, service_discovery_url):
        logger.debug("Updating service manager configuration ...")

        config_file_name = self.CONFIGS_FOLDER + self.SERVICE_MANAGER_CONFIG_FILENAME
        if not self.is_file_exist(config_file_name):
            config_file_name = BoardVirtual.PATH_SERVICE_MANAGER_CFG

        ret = self.read_file(config_file_name)

        try:
            config = json.loads(ret)
        except ValueError as e:
            logger.debug(e)
            raise BoardError("Failed to update service manager configuration.")
        try:
            if config["serviceDiscovery"] != service_discovery_url:
                logger.debug("Service discovery url: {} changing to: {}".format(
                    config["serviceDiscovery"],
                    service_discovery_url))
                config["serviceDiscovery"] = service_discovery_url
        except KeyError as e:
            logger.debug(e)
            raise BoardError("Failed to set service manager configuration")

        sm_cfg = json.dumps(config, indent=4)
        self.write_to_file(config_file_name, sm_cfg)

    def _restart_aos_services(self):
        logger.debug("Restarting services ...")

        for s in ("aos-vis", "aos-servicemanager", "aos-updatemanager"):
            logger.debug("Enabling %s ...", s)
            self.connector.execute("systemctl enable {}".format(s))
            logger.debug("Restarting %s ...", s)
            self.connector.execute("systemctl restart {}".format(s))

    def get_hw_id(self):
        """ Obtains a board HWID"""
        logger.info("Obtaining hardware ID ...")
        file_name = self.CONFIGS_FOLDER + self.HW_ID_FILE_NAME
        hw_id = self.read_file(file_name)

        if hw_id:
            return hw_id
        new_hw_id = str(uuid.uuid4())
        self.write_to_file(file_name, new_hw_id)
        return new_hw_id

    def get_vin(self):
        """ Obtains VIN. """
        logger.info("Obtaining VIN ...")
        vis_file_name = self.CONFIGS_FOLDER + self.VIS_CONFIG_FILENAME_2
        if not self.is_file_exist(vis_file_name):
            vis_file_name = self.CONFIGS_FOLDER + self.VIS_CONFIG_FILENAME_1
            if not self.is_file_exist(vis_file_name):
                vis_file_name = self.OLD_PATH_VIS_CFG

        vis_file_data = self.read_file(vis_file_name)
        if not vis_file_data:
            return None

        vin = None
        try:
            vis_data = json.loads(vis_file_data)
            for pos, a in enumerate(vis_data["Adapters"]):
                if BoardVirtual._STORAGE_ADAPTER in a["Plugin"]:
                    data = a["Params"]["Data"]
                    vin = data[BoardVirtual._KEY_VIN]["Value"]
                    if vin is not None and vin == "TestVIN":
                        vin = None
                    break
        except Exception:
            logger.warning("Can't read VIN for virtual board.")

        return vin

    def get_model_name(self):
        """ Obtains model name and version"""
        logger.info("Obtaining model name ...")

        model_name = self.read_file(self.CONFIGS_FOLDER + self.MODEL_FILE_NAME)

        if not model_name:
            logger.info(" .. model name is absent. Please update you VM image with a fresh copy!")
            return "VM test", "1.2"

        model_name_chunks = model_name.strip().split(";")
        model_name_name_chunk = model_name_chunks[0].strip()
        if len(model_name_chunks) > 1:
            model_name_version_chunk = model_name_chunks[1].strip()
        else:
            model_name_version_chunk = "0.1"

        logger.info(" .. model name: '{}' version: '{}'".format(model_name_name_chunk, model_name_version_chunk))
        return model_name_name_chunk, model_name_version_chunk

    def configure(self, cfg):
        logger.info("Configuring the board ...")
        self._set_certificates(cfg.online_certificate, cfg.offline_certificate, cfg)
        self._update_vis_config(cfg.vin, cfg.user_claim)
        self._update_service_manager_config(cfg.service_discovery_uri)
        self._restart_aos_services()

    def perform_deprovisioning(self):
        logger.info("Disabling service manager...")
        update_config = self.read_file(self.CONFIGS_FOLDER + self.UPDATE_MANAGER_CONFIG_FILENAME)

        if not update_config:
            update_config = self.read_file(self.OLD_PATH_UM_CFG)

        if not update_config:
            raise BoardError("Can't find Update Manager Config.")

        try:
            config = json.loads(update_config)
        except ValueError as e:
            logger.debug(e)
            raise BoardError("Failed to load update manager configuration.")
        board_config = Config
        board_config.online_key_folder = BoardVirtual.OLD_PATH_SM_CERTS
        board_config.online_key_filename = 'vehicle_offline.key.pem'
        board_config.online_cert_folder = BoardVirtual.OLD_PATH_SM_CERTS
        board_config.online_cert_filename = 'vehicle_offline.crt.pem'
        board_config.offline_key_folder = BoardVirtual.OLD_PATH_SM_CERTS
        board_config.offline_key_filename = 'vehicle_online.key.pem'
        board_config.offline_cert_folder = BoardVirtual.OLD_PATH_SM_CERTS
        board_config.offline_cert_filename = 'vehicle_online.crt.pem'

        crt_config = config.get("CrtModules", [])
        for item in crt_config:
            cert_folder = item.get("Params", {}).get("StoragePath")
            old_name_style = False
            if cert_folder and item.get("ID"):
                if item.get("ID") == 'online':
                    board_config.online_key_folder = cert_folder
                    board_config.online_cert_folder = cert_folder
                elif item.get("ID") == 'offline':
                    board_config.offline_key_folder = cert_folder
                    board_config.offline_cert_folder = cert_folder

        if self.is_file_exist(board_config.online_key_folder):
            self._delete_dir(board_config.online_key_folder)
        if self.is_file_exist(board_config.online_cert_folder):
            self._delete_dir(board_config.online_cert_folder)
        if self.is_file_exist(board_config.offline_key_folder):
            self._delete_dir(board_config.offline_key_folder)
        if self.is_file_exist(board_config.offline_cert_folder):
            self._delete_dir(board_config.offline_cert_folder)

        self.connector.execute("systemctl stop aos-servicemanager")
        self.connector.execute("systemctl disable aos-servicemanager")
        self.connector.execute("systemctl stop aos-updatemanaget")
        self.connector.execute("systemctl disable aos-updatemanaget")
        self.connector.execute("cd /var/aos/servicemanager && /usr/bin/aos_servicemanager -reset")
        logger.info("Deprovisioning process successfully finished!")
