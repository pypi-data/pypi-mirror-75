#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#

import json
import logging
import os
import time
import uuid

from aos_provisioning.onboard.board_base import BoardBase
from aos_provisioning.utils.connectors import SSHConnector
from aos_provisioning.utils.errors import BoardError, GenerateKeysError

logger = logging.getLogger(__name__)


class BoardVirtual(BoardBase):
    """Represent work with Virtual Board"""
    PATH_HW_ID = '/etc/guid'
    OLD_PATH_SM_CERTS = '/var/aos/servicemanager/data/fcrypt'
    OLD_PATH_VIS_CFG = '/var/aos/vis/visconfig.json'
    OLD_PATH_UM_CFG = '/var/aos/updatemanager/aos_updatemanager.cfg'
    OLD_PATH_SERVICE_MANAGER_CFG = '/var/aos/servicemanager/aos_servicemanager.cfg'

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

    def get_init_data(self):
        """ Read aos-updatemanager config on board and find in it places where to store certificates and keys.
            Find aos-servicemanager config and store it location in config.

            Raises:
                BoardError: If config file was not found on the board on known places.
            Returns:
                None
        """
        # Try to read config in new path
        um_config_path = os.path.join(self.CONFIGS_FOLDER, self.UPDATE_MANAGER_CONFIG_FILENAME)
        um_config_file = self.read_file(um_config_path)

        if not um_config_file:
            # Search for config in old path
            um_config_file = self.OLD_PATH_UM_CFG
            um_config_file = self.read_file(um_config_file)

        if not um_config_file:
            # Cant proceed further because config not found
            raise BoardError("Can't find Update Manager Config.")

        try:
            config = json.loads(um_config_file)
        except ValueError as e:
            logger.debug(e)
            raise BoardError("Failed to load update manager configuration. It is not a valid JSON.")

        # Default key names and directories are in old places
        self.config.online_key_folder = BoardVirtual.OLD_PATH_SM_CERTS
        self.config.online_key_filename = 'vehicle_online.key.pem'
        self.config.online_cert_folder = BoardVirtual.OLD_PATH_SM_CERTS
        self.config.online_cert_filename = 'vehicle_online.crt.pem'
        self.config.online_csr_filename = 'vehicle_online.csr.pem'
        self.config.offline_key_folder = BoardVirtual.OLD_PATH_SM_CERTS
        self.config.offline_key_filename = 'vehicle_offline.key.pem'
        self.config.offline_cert_folder = BoardVirtual.OLD_PATH_SM_CERTS
        self.config.offline_cert_filename = 'vehicle_offline.crt.pem'
        self.config.offline_csr_filename = 'vehicle_offline.csr.pem'

        # Change key names and directories with the config params
        crt_config = config.get("CrtModules", [])
        for item in crt_config:
            cert_folder = item.get("Params", {}).get("StoragePath")
            if cert_folder and item.get("ID"):
                if item.get("ID") == 'online':
                    self.config.online_key_folder = cert_folder
                    self.config.online_key_filename = 'unit_online.pem.key'
                    self.config.online_cert_folder = cert_folder
                    self.config.online_cert_filename = 'unit_online.pem.crt'
                    self.config.online_csr_filename = 'unit_online.pem.csr'
                elif item.get("ID") == 'offline':
                    self.config.offline_key_folder = cert_folder
                    self.config.offline_key_filename = 'unit_offline.pem.key'
                    self.config.offline_cert_folder = cert_folder
                    self.config.offline_cert_filename = 'unit_offline.pem.crt'
                    self.config.offline_csr_filename = 'unit_offline.pem.csr'

        if not self.config.online_key_folder.endswith("/"):
            self.config.online_key_folder = self.config.online_key_folder + '/'

        if not self.config.online_cert_folder.endswith("/"):
            self.config.online_cert_folder = self.config.online_cert_folder + '/'

        if not self.config.offline_key_folder.endswith("/"):
            self.config.offline_key_folder = self.config.offline_key_folder + '/'

        if not self.config.offline_cert_folder.endswith("/"):
            self.config.offline_cert_folder = self.config.offline_cert_folder + '/'

        sm_config_path = os.path.join(self.CONFIGS_FOLDER, self.SERVICE_MANAGER_CONFIG_FILENAME)
        if not self.is_file_exist(sm_config_path):
            sm_config_path = self.OLD_PATH_SERVICE_MANAGER_CFG
            if not self.is_file_exist(sm_config_path):
                raise BoardError("Can't find Service Manager Config.")
        self.config.service_manager_config_path = sm_config_path

        sm_config_file = self.read_file(self.config.service_manager_config_path)
        if not sm_config_file:
            # Cant proceed further because config not found
            raise BoardError("Can't find Service Manager Config.")

        try:
            config = json.loads(sm_config_file)
            self.config.target_resources_file_path = config.get('resourceConfigFile')
        except ValueError as e:
            logger.debug(e)
            raise BoardError("Failed to load update manager configuration. It is not a valid JSON.")

    def init_connector(self):
        ssh = SSHConnector(self._address, self._port, self._cred)
        ssh.connect()
        return ssh

    def _generate_pair(self, p_type):
        self.create_dir(self._config.online_key_folder)
        self.create_dir(self._config.online_cert_folder)
        self.create_dir(self._config.offline_key_folder)
        self.create_dir(self._config.offline_cert_folder)

        if p_type == 'online':
            key_filename = os.path.join(self._config.online_key_folder, self._config.online_key_filename)
            csr_filename = os.path.join(self._config.online_key_folder, self._config.online_csr_filename)
        elif p_type == 'offline':
            key_filename = os.path.join(self._config.offline_key_folder, self._config.offline_key_filename)
            csr_filename = os.path.join(self._config.offline_key_folder, self._config.offline_csr_filename)
        else:
            raise GenerateKeysError('Unknown key type while generating keys on board')

        key_gen_cmd = "openssl genrsa -out {file_name} 2048".format(file_name=key_filename)
        resp = self.connector.execute(key_gen_cmd)
        if resp.exit_code:
            logger.error('Failed to generate key.')
            raise BoardError("Failed to generate key.")

        cmd = "openssl req -new -key {key_name} -out {csr_name} -subj \"/CN=Unit Comm\"".format(
            key_name=key_filename,
            csr_name=csr_filename
        )

        resp = self.connector.execute(cmd)
        if resp.exit_code:
            logger.error('Failed to generate csr.')
            raise BoardError("Failed to generate csr.")

        return self.read_file(csr_filename)

    def _set_certificates(self):
        """ Saves certificates on board. """
        self.write_to_file(
            os.path.join(self.config.offline_cert_folder, self.config.offline_cert_filename),
            self.config.offline_certificate
        )
        self.write_to_file(
            os.path.join(self.config.online_cert_folder, self.config.online_cert_filename),
            self.config.online_certificate
        )

        online_csr = os.path.join(self.config.online_key_folder, self.config.online_csr_filename)
        self.delete_dir(online_csr, check_for_presence=True)

        offline_csr = os.path.join(self.config.offline_key_folder, self.config.offline_csr_filename)
        self.delete_dir(offline_csr, check_for_presence=True)

    def _set_target_resources(self):
        if self.config.target_resources:
            if not self.config.target_resources_file_path:
                raise BoardError("Can't find where to store resources config. Please update VM")
            self.write_to_file(self.config.target_resources_file_path, self.config.target_resources)

    _STORAGE_ADAPTER = 'storageadapter'
    _KEY_VIN = 'Attribute.Vehicle.VehicleIdentification.VIN'
    _KEY_CLAIM = 'Attribute.Vehicle.UserIdentification.Users'

    def _update_vis_config(self):
        logger.debug("Updating VIS configuration ...")

        ret = self.read_file(self.config.vis_config_path)

        try:
            config = json.loads(ret)
        except ValueError as e:
            logger.debug(e)
            raise BoardError("Failed to set VIS configuration.")

        try:
            for pos, a in enumerate(config['Adapters']):
                if BoardVirtual._STORAGE_ADAPTER in a['Plugin']:
                    data = a['Params']['Data']
                    data[BoardVirtual._KEY_VIN]['Value'] = self.config.system_id
                    data[BoardVirtual._KEY_CLAIM]['Value'] = [self.config.user_claim]
        except KeyError as e:
            logger.debug(e)
            raise BoardError("Failed to set VIS configuration")

        vis_cfg = json.dumps(config, indent=4)
        self.write_to_file(self.config.vis_config_path, vis_cfg)

    def _update_service_manager_config(self):
        logger.debug("Updating service manager configuration ...")
        logger.debug("SM path " + self.config.service_manager_config_path)
        ret = self.read_file(self.config.service_manager_config_path)
        service_discovery_url = self.config.service_discovery_uri
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
        self.write_to_file(self.config.service_manager_config_path, sm_cfg)

    def _restart_aos_services(self):
        logger.debug("Restarting services ...")

        for s in ("aos-vis", "aos-updatemanager", "aos-servicemanager"):
            print("Starting " + s)
            logger.debug("Enabling %s ...", s)
            self.connector.execute("systemctl enable {}".format(s))
            logger.debug("Restarting %s ...", s)
            self.connector.execute("systemctl restart {}".format(s))
            if s == 'aos-updatemanager':
                time.sleep(2)
            else:
                time.sleep(1)

    def get_hw_id(self):
        """ Obtains a board HWID.
        If HW is found, store it in config.
        If HW id is not found, generate it, store in config and write to the board.

            Returns:
                None
        """
        logger.info("Obtaining hardware ID ...")
        hw_id_file_name = os.path.join(self.CONFIGS_FOLDER, self.HW_ID_FILE_NAME)
        hw_id = self.read_file(hw_id_file_name)

        if hw_id:
            self._config.hw_id = hw_id
            return

        new_hw_id = str(uuid.uuid4())
        self.write_to_file(hw_id_file_name, new_hw_id)
        self._config.hw_id = new_hw_id

    def get_system_id(self):
        """ Obtains SystemID and stores it in config.

            Returns:
                None
        """
        logger.info("Obtaining System ID ...")
        vis_file_name = os.path.join(self.CONFIGS_FOLDER, self.VIS_CONFIG_FILENAME_2)
        if not self.is_file_exist(vis_file_name):
            vis_file_name = os.path.join(self.CONFIGS_FOLDER, self.VIS_CONFIG_FILENAME_1)
            if not self.is_file_exist(vis_file_name):
                vis_file_name = self.OLD_PATH_VIS_CFG

        vis_file_data = self.read_file(vis_file_name)
        if vis_file_data:
            self.config.vis_config_path = vis_file_name
            logger.debug('VIS config found in %s', vis_file_name)
        else:
            logger.debug('VIS config not found, so no SystemID either')
            return

        system_id = None
        try:
            vis_data = json.loads(vis_file_data)
            for pos, a in enumerate(vis_data["Adapters"]):
                if BoardVirtual._STORAGE_ADAPTER in a["Plugin"]:
                    data = a["Params"]["Data"]
                    system_id = data[BoardVirtual._KEY_VIN]["Value"]
                    if system_id is not None and system_id == "TestVIN":
                        system_id = None
                    break
        except Exception:
            logger.warning("Can't read System ID for virtual board.")
        self._config._system_id = system_id

    def get_model_name(self):
        """ Obtains board model name and version from board and store it in config

            Returns:
                None
        """
        logger.info("Obtaining model name ...")

        model_name = self.read_file(self.CONFIGS_FOLDER + self.MODEL_FILE_NAME)

        if not model_name:
            logger.info(" .. model name is absent. Please update you VM image with a fresh copy!")
            self._config.model_name = "VM test"
            self._config.model_version = "Unknown"
            return

        model_name_chunks = model_name.strip().split(";")
        model_name_name_chunk = model_name_chunks[0].strip()
        if len(model_name_chunks) > 1:
            model_name_version_chunk = model_name_chunks[1].strip()
        else:
            model_name_version_chunk = "0.1"

        logger.info(" .. model name: '{}' version: '{}'".format(model_name_name_chunk, model_name_version_chunk))
        self._config.model_name = model_name_name_chunk
        self._config.model_version = model_name_version_chunk
        return

    def configure(self):
        logger.info("Configuring the board ...")
        self._set_target_resources()
        self._set_certificates()
        self._update_vis_config()
        self._update_service_manager_config()
        self._restart_aos_services()

    def perform_deprovisioning(self):
        logger.info("Disabling unit services...")

        self.connector.execute("systemctl stop aos-servicemanager")
        self.connector.execute("systemctl disable aos-servicemanager")
        self.connector.execute("systemctl stop aos-updatemanaget")
        self.connector.execute("systemctl disable aos-updatemanaget")
        self.connector.execute("cd /var/aos/servicemanager && /usr/bin/aos_servicemanager -reset")
        self.delete_dir(self.config.online_key_folder, check_for_presence=True)
        self.delete_dir(self.config.online_cert_folder, check_for_presence=True)
        self.delete_dir(self.config.offline_key_folder, check_for_presence=True)
        self.delete_dir(self.config.offline_cert_folder, check_for_presence=True)

        logger.info("Deprovisioning process successfully finished!")
