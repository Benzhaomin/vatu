import logging
from typing import List

from vatu.config import Config


def sudo_cat(filepath) -> List[str]:
    """ Reads *filepath* using sudo
    """
    logging.debug('sudo cat %s', filepath)

    with open(filepath) as f:
        return f.readlines()


def sudo_tee(filepath, string):
    """ Writes *string* to *filepath* unless we are in read-only mode
    """
    logging.debug('echo %s | sudo tee %s', string, filepath)

    if Config.get('readonly'):
        logging.debug("read-only, we didn't actually write anything but feel free to execute that command as root")
        return

    # how much sanitizing can one really need
    with open(filepath, 'w') as f:
        print(string, file=f)


def sudo_tee_a(filepath, string):
    """ Appends *string* to *filepath* unless we are in read-only mode
    """
    logging.debug('echo %s | sudo tee -a %s', string, filepath)

    if Config.get("readonly"):
        logging.debug("read-only, we didn't actually append anything but feel free to execute that command as root")
        return

    # how much sanitizing can one really need
    with open(filepath, 'a') as f:
        print(string, file=f)
