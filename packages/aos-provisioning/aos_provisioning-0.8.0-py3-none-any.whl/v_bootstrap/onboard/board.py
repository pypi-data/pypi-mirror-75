#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#

import hashlib
import logging
import time
import uuid

from v_bootstrap.onboard.board_base import BoardBase
from v_bootstrap.utils.connectors import SerialConnector

logger = logging.getLogger(__name__)


class Board(BoardBase):
    PATH_VIN = '/var/aos/vin'

    def __init__(self, port, cred):
        super(Board, self).__init__()
        self._port = port
        self._cred = cred

    def init_connector(self):
        serial = SerialConnector(self._port, self._cred)
        serial.connect()

        return serial

    def get_hw_id(self):
        logger.info("Obtaining hardware ID ...")
        hw_id = self._read_hw_id()
        return hw_id

    def get_vin(self):
        logger.info("Obtaining vin ...")
        if not self._is_vin_defined():
            logger.info("VIN not found.... Initializing board ")
            if not self._is_file_exist("/var/aos"):
                self.connector.execute_script("mkdir /var/aos")
            self.connector.execute_script("/xt/scripts/aos-provisioning.step2.sh get_vin")
            logger.info("Script done")
        if self._is_vin_defined():
            return self._cat_file(self.PATH_VIN, 17, True)
        else:
            logger.error("VIN not defined")
            return None

    def _is_vin_defined(self):
        ret = self.connector.execute("test -e {}".format(Board.PATH_VIN))
        return not ret.exit_code

    def _is_file_exist(self, filename):
        ret = self.connector.execute("test -e {}".format(filename))
        return not ret.exit_code

    def _is_model_name_file_present(self):
        """ Checks presence if model name file. """
        ret = self.connector.execute(
            "test -e {}".format(BoardBase.PATH_MODEL_NAME))
        if ret.exit_code:
            return False

        return True

    def _validate_content_upload(self, content, target_file_name, add_new_line=False):
        target_checksum = self._read_checksum(target_file_name)
        if not target_checksum:
            return False

        m = hashlib.sha1()
        m.update(content.encode('utf-8'))
        if add_new_line:
            m.update('\n'.encode('utf-8'))

        logger.debug("Content digest is {}, Board file digest is {}".format(m.hexdigest(), target_checksum))

        return m.hexdigest() == target_checksum

    def _read_checksum(self, filename):
        """ Calculate file checksum on board. """
        ret = self.connector.execute("sha1sum {}".format(filename))
        if ret.exit_code:
            return False

        splitted = list(filter(None, ret.data.split(" ")))
        if len(splitted) == 2 and splitted[1] == filename:
            logger.debug("received checksum: {}".format(splitted[0]))
            return splitted[0]

        return False

    def _cat_file(self, filename, file_len, allow_empty=False):
        while True:
            try:
                ret = self.connector.execute("cat {}".format(filename))
                if ret.exit_code:
                    logger.error('Failed to get {} from the board'.format(filename))
                    raise AssertionError
                result = ret.data
                if len(result) != file_len:
                    if not len(result) and allow_empty:
                        return ""
                    time.sleep(0.5)
                else:
                    return result
            except ValueError:
                pass

    def _echo_to_file(self, filename, content, retry_count=5):
        cmd = "echo '{}' > {}".format(content, filename)
        try:
            logger.info("Uploading file {}.".format(filename))
            retry_count -= 1
            self.connector.execute(cmd, debug=False)
            while retry_count > 0 and not self._validate_content_upload(content, filename, True):
                logger.info("Upload file {} failed. Retry count left {}".format(filename, retry_count))
                self.connector.execute(cmd, debug=False)
                retry_count -= 1
        except ValueError:
            pass

    def _read_hw_id(self):
        tmp_guid = str(uuid.uuid4())

        logger.debug("Running AOS provisioning script STEP1")
        while True:
            try:
                ret = self.connector.execute_script("/xt/scripts/aos-provisioning.step1.sh")
                if ret.exit_code:
                    logger.error("Failed to run AOS provisioning script STEP1")
                    raise AssertionError
                break
            except ValueError:
                pass
        logger.debug("AOS provisioning script STEP1 successful finished")

        result = self._cat_file("/var/aos/hwid", len(tmp_guid) - 4)
        return result

    def _generate_pair(self, pair_type):
        result = self._cat_file("/var/aos/{}.pub.pem".format(pair_type), 450)
        return result

    def _save_cert_to_file(self, file_name, file_content):
        logger.info("Upload cert {} to board".format(file_name))
        _CERT_END = "-----END CERTIFICATE-----\n"
        _CERT_END_NOT_NL = "-----END CERTIFICATE-----"

        chunks = file_content.split(_CERT_END)

        while True:
            try:
                self.connector.execute("rm -f {}".format(file_name), debug=False)
            except ValueError:
                pass

            for chunk in chunks:
                if chunk not in [_CERT_END, _CERT_END_NOT_NL, ""]:
                    cmd = "echo '{}' >> {}".format(chunk + _CERT_END_NOT_NL, file_name)
                    self.connector.send(cmd)
            time.sleep(1.5)
            self.connector.send("\x03")
            time.sleep(1)
            self.connector.execute('clear')
            self.connector.clear()

            resp = self.connector.execute("test -e {}".format(file_name))
            if resp.exit_code:
                logger.error("Uploaded file not found. Retrying upload...")
                continue

            if not self._validate_content_upload(file_content, file_name):
                logger.error("Uploaded file checksum is wrong. Retrying upload...")
                continue
            else:
                logger.info("File {} uploaded successfully.".format(file_name))
                break

    def configure(self, cfg):
        logger.info("Configuring the board ...")
        logger.debug("Putting certificates...")
        self._save_cert_to_file("/var/aos/online.crt.pem", cfg.online_certificate)
        self._save_cert_to_file("/var/aos/offline.crt.pem", cfg.offline_certificate)
        time.sleep(1)
        logger.debug("Putting info...")
        self._echo_to_file("/var/aos/vin", cfg.vin)
        self._echo_to_file("/var/aos/claim", cfg.user_claim)
        self._echo_to_file("/var/aos/sm_service_discovery", cfg.service_discovery_uri)

        logger.debug("Running AOS provisioning script STEP2")
        while True:
            try:
                ret = self.connector.execute_script("/xt/scripts/aos-provisioning.step2.sh")
                if ret.exit_code:
                    logger.error("Failed to run AOS provisioning script STEP2")
                    raise AssertionError
                break
            except ValueError:
                pass
        logger.debug("AOS provisioning script STEP2 successful finished")

    def perform_deprovisioning(self):
        logger.debug("Running AOS deprovisioning script")
        while True:
            try:
                ret = self.connector.execute_script("/xt/scripts/aos-provisioning.step2.sh deprovisioning")
                if ret.exit_code:
                    logger.error("Failed to run AOS deprovisioning script")
                    raise AssertionError
                break
            except ValueError:
                pass
        logger.debug("AOS deprovisioning script successful finished")

    def get_model_name(self):
        """ Obtains model name and version"""
        logger.info("Obtaining model name ...")

        if self._is_model_name_file_present():
            model_name = self.connector.execute("cat %s" % self.PATH_MODEL_NAME).data
        else:
            model_name = "Dev board; 1.0"

        if isinstance(model_name, bytes):
            model_name = model_name.decode()

        if not model_name:
            logger.info(" .. model name is absent. Please update you VM image with a fresh copy!")
            return "VM test", "0.1"

        model_name_chunks = model_name.strip().split(";")
        model_name_name_chunk = model_name_chunks[0].strip()
        if len(model_name_chunks) > 1:
            model_name_version_chunk = model_name_chunks[1].strip()
        else:
            model_name_version_chunk = "0.1"

        logger.info(" .. model name: '{}' version: '{}'".format(model_name_name_chunk, model_name_version_chunk))
        return model_name_name_chunk, model_name_version_chunk
