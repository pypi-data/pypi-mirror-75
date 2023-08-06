#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#

from aos_provisioning.utils.errors import ConfigValidationError


class Config(object):
    """ Contains a board configuration. """

    def __init__(self):
        self._hw_id = None
        self._vin = None
        self._system_id = None
        self._keys = None
        self._model = None
        self._manufacturer = None
        self._online_cert = None
        self._offline_cert = None
        self._user_claim = None
        self._discovery_uri = None

        self._service_manager_config_path = None
        self._vis_config_path = None

        self._model_name = None
        self._model_version = None

        self._offline_key_folder = None
        self._offline_key_filename = None
        self._offline_cert_folder = None
        self._offline_cert_filename = None
        self._offline_csr_filename = None

        self._online_key_folder = None
        self._online_key_filename = None
        self._online_cert_folder = None
        self._online_cert_filename = None
        self._online_csr_filename = None

        self._target_resources = None
        self._target_resources_file_path = None

    @property
    def service_manager_config_path(self):
        return self._service_manager_config_path

    @service_manager_config_path.setter
    def service_manager_config_path(self, value):
        self._service_manager_config_path = value

    @property
    def vis_config_path(self):
        return self._vis_config_path

    @vis_config_path.setter
    def vis_config_path(self, value):
        self._vis_config_path = value

    @property
    def hw_id(self):
        return self._hw_id

    @hw_id.setter
    def hw_id(self, value):
        self._hw_id = value

    @property
    def vin(self):
        return self._vin

    @vin.setter
    def vin(self, value):
        self._vin = value

    @property
    def system_id(self):
        return self._system_id

    @system_id.setter
    def system_id(self, value):
        self._system_id = value

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def manufacturer(self):
        return self._manufacturer

    @manufacturer.setter
    def manufacturer(self, value):
        self._manufacturer = value

    @property
    def model_name(self):
        return self._model_name

    @model_name.setter
    def model_name(self, value):
        self._model_name = value

    @property
    def model_version(self):
        return self._model_version

    @model_version.setter
    def model_version(self, value):
        self._model_version = value

    @property
    def offline_certificate(self):
        return self._offline_cert

    @offline_certificate.setter
    def offline_certificate(self, value):
        self._offline_cert = value

    @property
    def online_certificate(self):
        return self._online_cert

    @online_certificate.setter
    def online_certificate(self, value):
        self._online_cert = value

    @property
    def user_claim(self):
        return self._user_claim

    @user_claim.setter
    def user_claim(self, value):
        self._user_claim = value

    def set_keys(self, keys):
        self._keys = keys

    def get_public_online(self):
        return self._keys.online

    def get_public_offline(self):
        return self._keys.offline

    @property
    def service_discovery_uri(self):
        return self._discovery_uri

    @service_discovery_uri.setter
    def service_discovery_uri(self, value):
        self._discovery_uri = value

    @property
    def online_key_folder(self):
        return self._online_key_folder

    @online_key_folder.setter
    def online_key_folder(self, value):
        self._online_key_folder = value

    @property
    def online_key_filename(self):
        return self._online_key_filename

    @online_key_filename.setter
    def online_key_filename(self, value):
        self._online_key_filename = value

    @property
    def online_cert_folder(self):
        return self._online_cert_folder

    @online_cert_folder.setter
    def online_cert_folder(self, value):
        self._online_cert_folder = value

    @property
    def online_cert_filename(self):
        return self._online_cert_filename

    @online_cert_filename.setter
    def online_cert_filename(self, value):
        self._online_cert_filename = value

    @property
    def online_csr_filename(self):
        return self._online_csr_filename

    @online_csr_filename.setter
    def online_csr_filename(self, value):
        self._online_csr_filename = value

    @property
    def offline_key_folder(self):
        return self._offline_key_folder

    @offline_key_folder.setter
    def offline_key_folder(self, value):
        self._offline_key_folder = value

    @property
    def offline_key_filename(self):
        return self._offline_key_filename

    @offline_key_filename.setter
    def offline_key_filename(self, value):
        self._offline_key_filename = value

    @property
    def offline_cert_folder(self):
        return self._offline_cert_folder

    @offline_cert_folder.setter
    def offline_cert_folder(self, value):
        self._offline_cert_folder = value

    @property
    def offline_cert_filename(self):
        return self._offline_cert_filename

    @offline_cert_filename.setter
    def offline_cert_filename(self, value):
        self._offline_cert_filename = value

    @property
    def offline_csr_filename(self):
        return self._offline_csr_filename

    @offline_csr_filename.setter
    def offline_csr_filename(self, value):
        self._offline_csr_filename = value

    @property
    def target_resources(self):
        return self._target_resources

    @target_resources.setter
    def target_resources(self, value):
        self._target_resources = value

    @property
    def target_resources_file_path(self):
        return self._target_resources_file_path

    @target_resources_file_path.setter
    def target_resources_file_path(self, value):
        self._target_resources_file_path = value

    def validate(self):
        if self.system_id is None:
            raise ConfigValidationError("System Id is not set.")

        if self.offline_certificate is None:
            raise ConfigValidationError("Offline certificate is not defined.")

        if self.online_certificate is None:
            raise ConfigValidationError("Online certificate is not defined.")

        if self.user_claim is None:
            raise ConfigValidationError("User claim is not defined.")
