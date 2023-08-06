#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#

import argparse
import logging
import os
import sys
import time

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from aos_provisioning import __version__
from aos_provisioning.onboard.board import Board
from aos_provisioning.onboard.board_virtual import BoardVirtual
from aos_provisioning.utils import security, yes_no, get_serial_devices, check_access_to_serial_ports
from aos_provisioning.utils.cloud_api import CloudAPI
from aos_provisioning.utils.errors import OnBoardingError, DeviceDeregisterError, CloudAccessError
from aos_provisioning.utils.logs import init_bootstrap_log

logger = logging.getLogger(__name__)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

try:
    # Revert monkey patch introduced error on loading certificate chain
    requests.packages.urllib3.contrib.pyopenssl.extract_from_urllib3()
except:
    pass


_COMMAND_BOARD_WHICH = 'board'
_COMMAND_VIRTUAL_BOARD_WHICH = 'virt-board'
_COMMAND_DEPROVISIONING = 'deprovision-virt-board'
_COMMAND_BOARD_DEPROVISIONING = 'deprovision-board'


class SubParserHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def _format_action(self, action):
        """ Handles sub commands. """
        s_class = super(argparse.RawDescriptionHelpFormatter, self)
        parts = s_class._format_action(action)

        if action.nargs == argparse.PARSER:
            parts = "\n".join(parts.split("\n")[1:])

        return parts


def _parse_args():
    def _validate_file(source):
        """ Validates an identity file. """
        if not os.path.isfile(source):
            mess = "Identity file {} not accessible."
            raise argparse.ArgumentTypeError(mess.format(source))

        return source

    parser = argparse.ArgumentParser(
        description="The board provisioning tool",
        formatter_class=SubParserHelpFormatter,
        epilog="Run 'aos-provisioning COMMAND --help' for more information on a command.")
    parser.set_defaults(which=None)

    parser.add_argument('--register-host', default=CloudAPI.DEFAULT_REGISTER_HOST,
                        help="Host address to register. Default: {}".format(
                            CloudAPI.DEFAULT_REGISTER_PORT))
    parser.add_argument('--register-port', default=CloudAPI.DEFAULT_REGISTER_PORT,
                        help="Port to register. Default: {}".format(
                            CloudAPI.DEFAULT_REGISTER_PORT))
    parser.add_argument(
        '--cert', default=security.default_cert(), type=_validate_file,
        help="Certificate file. Default: {}".format(security.default_cert()))

    parser.add_argument('-u', '--user', default='root', help="Specifies the user to log in as on the remote board.")
    parser.add_argument('-p', '--password', default='Password1', help="User password.")

    # Commands
    sub_parser = parser.add_subparsers(title='Commands')

    # Board provisioning
    board = sub_parser.add_parser(_COMMAND_BOARD_WHICH, help='Launch a board provisioning procedure.')
    board.add_argument('--serial-port', default=None, help="Board serial port (optional).")
    board.set_defaults(which=_COMMAND_BOARD_WHICH)

    # Board deprovisioning
    board = sub_parser.add_parser(_COMMAND_BOARD_DEPROVISIONING, help='Launch a board deprovisioning procedure.')
    board.add_argument('--serial-port', default=None, help="Board serial port (optional).")
    board.set_defaults(which=_COMMAND_BOARD_DEPROVISIONING)

    # Virtual board provisioning
    virt_board = sub_parser.add_parser(
        _COMMAND_VIRTUAL_BOARD_WHICH,
        help='Launch a virtual board provisioning procedure.'
    )

    virt_board.add_argument('--host', default='127.0.0.1', help="Virtual board host name or IP. Default: 127.0.0.1")
    virt_board.add_argument('--port', default=2222, help="Virtual board port. Default: 2222")
    virt_board.set_defaults(which=_COMMAND_VIRTUAL_BOARD_WHICH)

    # Deprovisioning
    deprovisioning = sub_parser.add_parser(_COMMAND_DEPROVISIONING, help='Launch a deprovisioning procedure.')
    deprovisioning.add_argument('--host', default='127.0.0.1', help="Virtual board host name or IP. Default: 127.0.0.1")
    deprovisioning.add_argument('--port', default=2222, help="Virtual board port. Default: 2222")
    deprovisioning.set_defaults(which=_COMMAND_DEPROVISIONING)

    args = parser.parse_args()
    if args.which is None:
        parser.print_help()
        sys.exit(0)
    return args


def _detect_device(ports):
    """ Detects a new device. """
    ports = set(ports)
    while True:
        new_devs = list(get_serial_devices())
        new_ports = set([d.device for d in new_devs])
        detected = ports ^ new_ports

        if detected:
            port = detected.pop()
            for d in new_devs:
                if d.device == port:
                    return d

        time.sleep(.5)


def run_provisioning(board, cloud_api):
    """ Launches the bootstrapping procedure. """
    log_file = init_bootstrap_log()
    logger.info("Starting the provision procedure ... "
                "find the whole log info in %s", log_file)

    try:
        b = board()
        with b:
            b.get_init_data()
            b.get_model_name()
            b.get_hw_id()
            b.get_system_id()
            b.generate_pkeys()




        register_payload = {
            'hardware_id': b.config.hw_id,
            'online_public_csr': b.config.get_public_online(),
            'offline_public_csr': b.config.get_public_offline(),
            'board_model_name': b.config.model_name,
            'board_model_version': b.config.model_version,
            'provisioning_software': "aos-provisioning:{version}".format(version=__version__),
        }

        if b.config:
            register_payload['system_uid'] = b.config.system_id

        res = cloud_api.register_device(register_payload)
        b.config.system_id = res.get('system_uid')
        b.config.online_certificate = res.get('online_certificate')
        b.config.offline_certificate = res.get('offline_certificate')
        b.config.user_claim = res.get('claim')
        b.config.model = res.get('model')
        b.config.manufacturer = res.get('manufacturer')
        b.config.service_discovery_uri = cloud_api.service_discovery_url
        b.config.target_resources = res.get('target_resources')
        b.config.validate()

        # configure the board
        with b:
            b.configure()

        logger.info("Unit with System UID:%s has registered successfully.", b.config.system_id)
    except OnBoardingError as e:
        print(e)
        logger.error('\nUnable to provision the board:\n%s', str(e))
        return 1
    except KeyboardInterrupt:
        logger.info('\nExiting ...')
        return 1

    return 0


def run_deprovisioning(board, cloud_api):
    """ Launches the deprovisioning procedure."""
    log_file = init_bootstrap_log()
    logger.info("Starting the deprovision procedure ... \nfind the whole log info in %s", log_file)

    b = board()
    with b:
        b.get_init_data()
        b.get_system_id()
        b.get_hw_id()

    payload = {
        "system_uid": b.config.system_id,
        'provisioning_software': "v-bootstrap:{version}".format(version=__version__)
    }

    try:
        logger.info("Deprovisioning the board ...")
        cloud_api.deregister_device(payload)
        logger.info("Board with HW id '{hw}' and unit '{system_id}' has deregistered successfully".format(
            hw=b.config.hw_id,
            system_id=b.config.system_id
        ))
    except DeviceDeregisterError as e:
        logger.debug(e)
        logger.error("Failed to deprovision board.")
        return 1

    with b:
        b.perform_deprovisioning()

    return 0


def _init_board(board, *args, **kwargs):
    """ Initializes a board instance. """

    def _wrap():
        return board(*args, **kwargs)

    return _wrap


def main():
    """ The main entry point. """
    status = 0
    args = _parse_args()
    cred = args.user, args.password

    try:
        if not security.keys_exist():
            sys.stdout.write('Failed to find a key pair '
                             'in {}.\n'.format(security.get_security_dir()))
            raise AssertionError

        cloud_api = CloudAPI(args.cert, args.register_host, args.register_port)
        cloud_api.check_cloud_access()

        if args.which == _COMMAND_BOARD_WHICH:

            sys.stdout.write("Starting board provisioning procedure...\n")
            check_access_to_serial_ports()

            serial_port_name = args.serial_port

            if serial_port_name is None:

                mess = "Please make sure that device is not plugged in.\n" \
                       "Unplug device before continue"
                if not yes_no(mess, "yes"):
                    raise AssertionError

                devices = get_serial_devices()
                sys.stdout.write("Please plug-in device. Waiting for ...\n")

                ports = [d.device for d in devices]
                dev = _detect_device(ports)

                mess = "{} device detected. Continue:".format(str(dev))
                if not yes_no(mess):
                    raise AssertionError

                mess = "Please, switch on your device \n" \
                       "  using the button near the sticker 'StarterKit'\n" \
                       "  and wait for 5 seconds, then press 'y'\n"
                if not yes_no(mess):
                    raise AssertionError

                board = _init_board(Board, dev.device, cred)

            else:
                board = _init_board(Board, serial_port_name, cred)

            if board:
                status = run_provisioning(board, cloud_api)

        elif args.which == _COMMAND_VIRTUAL_BOARD_WHICH:
            sys.stdout.write("Starting virtual board provisioning procedure...\n")
            board = _init_board(BoardVirtual, args.host, args.port, cred)
            if board:
                status = run_provisioning(board, cloud_api)

        elif args.which == _COMMAND_DEPROVISIONING:
            sys.stdout.write("Starting virtual board deprovisioning procedure...\n")
            board = _init_board(BoardVirtual, args.host, args.port, cred)
            if board:
                status = run_deprovisioning(board, cloud_api)

        elif args.which == _COMMAND_BOARD_DEPROVISIONING:
            sys.stdout.write("Starting board deprovisioning procedure...\n")
            check_access_to_serial_ports()

            serial_port_name = args.serial_port

            if serial_port_name is None:

                mess = "Please make sure that device is not plugged in.\n" \
                       "Unplug device before continue"
                if not yes_no(mess, "yes"):
                    raise AssertionError

                devices = get_serial_devices()
                sys.stdout.write("Please plug-in device. Waiting for ...\n")

                ports = [d.device for d in devices]
                dev = _detect_device(ports)

                mess = "{} device detected. Continue:".format(str(dev))
                if not yes_no(mess):
                    raise AssertionError

                mess = "Please, switch on your device \n" \
                       "  using the button near the sticker 'StarterKit'\n" \
                       "  and wait for 5 seconds, then press 'y'\n"
                if not yes_no(mess):
                    raise AssertionError

                board = _init_board(Board, dev.device, cred)

            else:
                board = _init_board(Board, serial_port_name, cred)

            if board:
                status = run_deprovisioning(board, cloud_api)
    except CloudAccessError as e:
        logger.error('\nUnable to provision the board with error:\n%s', str(e))
        return 1

    except (AssertionError, KeyboardInterrupt):
        sys.stdout.write('Exiting ...\n')
        status = 1

    sys.exit(status)


if __name__ == '__main__':
    main()
