#
#  Copyright (c) 2018-2019 Renesas Inc.
#  Copyright (c) 2018-2019 EPAM Systems Inc.
#

import os
import platform
import sys
import logging

try:
    input = raw_input
except NameError:
    pass

logger = logging.getLogger(__name__)

from serial.tools import list_ports

_VBOOT_TOOL_DIR = '.aos'


def get_home_dir():
    """ Detects home dir for current user. """
    return os.path.expanduser("~")


def get_tool_dir():
    """ Returns a working dir. """
    return os.path.join(get_home_dir(), _VBOOT_TOOL_DIR)


def get_serial_devices():
    """ Gathers available devices. """
    return list_ports.comports()


def yes_no(message, answer='yes'):
    """ Shows a confirmation message. """
    yes = True, '[Y/n]'
    no = False, '[y/N]'

    answers = {'yes': yes, 'y': yes, 'no': no, 'n': no}

    if answer not in answers:
        raise ValueError("Invalid answer: {}".format(answer))

    status, prompt = answers[answer]

    while True:
        sys.stdout.write("{} {}: ".format(message, prompt))
        sign = input().lower().strip()

        if sign == '':
            break

        if sign in answers:
            status, prompt = answers[sign]
            break

    return status


def check_access_to_serial_ports():
    if platform.system() != "Linux":
        return True

    if os.getuid() == 0:
        # We run under sudo or root
        return True

    import grp
    import subprocess

    user_name = os.getlogin()
    user_groups = [g.gr_name for g in grp.getgrall() if user_name in g.gr_mem]

    if 'dialout' not in user_groups:
        # We need to add current user to group dialout
        # Check for rights for sudo
        if 'sudo' not in user_groups:
            sys.stdout.write('In Linux to access to serial ports you should be in group "dialout".\n'
                             'Contact your system administrator to add you to the group\n')
            raise AssertionError

        sys.stdout.write('Try to add your username to the "dialout" group using sudo.\n'
                         'Please enter your password if it will be asked\n')

        cmd = "sudo usermod -a -G dialout {}".format(user_name)
        ret_code = subprocess.call(cmd, shell=True, stdout=sys.stdout, stdin=sys.stdin, stderr=sys.stderr)
        if ret_code:
            logger.error("Error adding user to dialout group")
            raise AssertionError
        logger.info("User successfully added to dialout group")
        sys.stdout.write("User successfully added to dialout group\n")

    # get dialout group id
    dialout_group_id = int(grp.getgrnam('dialout')[2])

    if dialout_group_id not in os.getgroups():
        # We need to restart script with su - tuk

        sys.stdout.write('Before rights to dialout will be accessible you should relogin.\n'
                         'Now new shell session will be started (this may asks you for password one more time\n')

        python_cmd = sys.executable
        args = ["-i", "-g", "dialout", "-u", user_name, python_cmd, *sys.argv]
        ret_code = subprocess.call(args, executable="sudo", shell=False, stdout=sys.stdout, stdin=sys.stdin, stderr=sys.stderr)
        sys.exit(ret_code)

    return True