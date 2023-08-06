#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#

import logging

import OpenSSL
import requests

from aos_provisioning.utils.errors import DeviceRegisterError, CloudAccessError, DeviceDeregisterError
from aos_provisioning.utils.security import merge_certs

logger = logging.getLogger(__name__)


class CloudAPI(object):
    DEFAULT_REGISTER_HOST = 'aoscloud.io'
    DEFAULT_REGISTER_PORT = 10000

    __REGISTER_URI_TPL = 'https://{}:{}/api/v1/units/provisioning/'
    __DEPROVISIONING_URI_TPL = 'https://{}:{}/api/v1/units/deprovisioning/'
    __USER_ME_URI_TPL = 'https://{}:{}/api/v1/users/me/'
    __SERVICE_DISCOVERY_URI_TPL = 'https://{}:9000'

    def __init__(self, user_certificate_path, cloud_api_host=None, cloud_api_port=None):
        self._cloud_api_host = cloud_api_host if cloud_api_host else self.DEFAULT_REGISTER_HOST
        self._cloud_api_port = cloud_api_port if cloud_api_port else self.DEFAULT_REGISTER_PORT
        self._user_certificate_path = user_certificate_path
        self._user_credentials = merge_certs(self._user_certificate_path)

    @property
    def service_discovery_url(self) -> str:
        """Returns fully formatted service discovery URL ready to be written to a board"""
        return self.__SERVICE_DISCOVERY_URI_TPL.format(self._cloud_api_host)

    def check_cloud_access(self) -> None:
        """ Check user have access to the cloud and his role is OEM.

            Raises:
                CloudAccessError: If user haven't access to the cloud or his role is not OEM.
            Returns:
                None
        """
        try:
            url = self.__USER_ME_URI_TPL.format(self._cloud_api_host, self._cloud_api_port)
            resp = requests.get(url, verify=False, cert=self._user_credentials)
            if resp.status_code != 200:
                logger.debug('Auth error: {}'.format(resp.text))
                # print()
                raise CloudAccessError('You do not have access to the cloud!')

            user_info = resp.json()
            if user_info['role'] != 'oem':
                logger.debug('invalid user role'.format(resp.text))
                # print()
                raise CloudAccessError('You should use OEM account!')

            print('Operation will be executed using OEM account: "{}/{}"\n'.format(
                user_info['username'],
                user_info['oem']['title']
            ))
        except (requests.exceptions.RequestException, ValueError, OSError, OpenSSL.SSL.Error) as e:
            logger.error('Check access exception: {}'.format(e))

    def register_device(self, payload):
        """ Registers device in cloud. Returns registered metadata.
        :param: str - end_point for registering
        :param: str - path to server pem that contains certs and a private one
        :param: dict
        :return: dict
        """
        logger.info("Registering the board ...")
        end_point = self.__REGISTER_URI_TPL.format(self._cloud_api_host, self._cloud_api_port)

        try:
            logger.debug("Sending to %s payload: %s", end_point, payload)
            ret = requests.post(end_point, data=payload, verify=False, cert=self._user_credentials)
            if ret.status_code == 400:
                try:
                    resp_content = ret.content.decode()

                    try:
                        answer = ret.json()['non_field_errors'][0]
                        logger.info('Registration error: ' + answer)
                    except:
                        pass

                except UnicodeDecodeError:
                    resp_content = ret.content
                logger.debug("Cloud response: {}".format(resp_content))
            ret.raise_for_status()
            response = ret.json()
        except (requests.exceptions.RequestException,
                ValueError, OSError, OpenSSL.SSL.Error) as e:
            logger.debug(e)
            raise DeviceRegisterError("Failed to register board.")

        return response

    def deregister_device(self, payload):
        end_point = self.__DEPROVISIONING_URI_TPL.format(self._cloud_api_host, self._cloud_api_port)

        try:
            response = requests.delete(end_point, data=payload, verify=False, cert=self._user_credentials)
            if response.status_code == 400:
                try:
                    resp_content = response.content.decode()
                    try:
                        answer = response.json()['non_field_errors'][0]
                        logger.info('Deprovisioning error: ' + answer)
                    except:
                        pass
                except UnicodeDecodeError:
                    resp_content = response.content
                logger.debug("Cloud response: {}".format(resp_content))
            response.raise_for_status()
        except (requests.exceptions.RequestException,
                ValueError, OSError, OpenSSL.SSL.Error) as e:
            logger.debug(e)
            logger.error("Failed to deprovision board.")
            raise DeviceDeregisterError