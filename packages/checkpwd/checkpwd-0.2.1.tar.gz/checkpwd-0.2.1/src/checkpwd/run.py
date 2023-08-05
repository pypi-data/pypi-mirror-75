# Main file for the PwnedCheck distribution.
# This file retrieves the password, calls the module check_pwd,
# and check if the password has been breached by checking it with
# the database in the following website
# https://haveibeenpwned.com/Passwords

import sys
import logging
from getpass import getpass
from checkpwd.check_pwd import check_pwd

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def splash():
    """Splash `pwnedcheck` logo and information."""
    print(" _____________________________________________________ ")
    print("|   ____ _               _    ____              _     |")
    print("|  / ___| |__   ___  ___| | _|  _ \__      ____| |    |")  
    print("| | |   | '_ \ / _ \/ __| |/ / |_) \ \ /\ / / _` |    |")
    print("| | |___| | | |  __/ (__|   <|  __/ \ V  V / (_| |    |")
    print("|  \____|_| |_|\___|\___|_|\_\_|     \_/\_/ \__,_|    |")
    print("|                                                     |")
    print("| Author: Tanjona R. Rabemananjara                    |")
    print("| URL: https://radonirinaunimi.github.io/pwnd-check/  |")
    print("|_____________________________________________________|")


def main():
    """Function that fetchs the password given by the user from the command
    line using `getpass`. The password is then checked on `HaveIBeenPwned`.
    """
    splash()
    print("\nEnter your password below.")
    pwd = getpass()
    try:
        # Check the pwd and add the values to some variables
        hashed_pwd, nb_match = check_pwd(pwd)
        # Print the result
        if nb_match:
            print(f"The password occurs {nb_match} times (hash: {hashed_pwd})")
        else:
            print("Your password was not found")
    except UnicodeError:
        errormsg = sys.exc_info()[1]
        log.warning(f"Your password could not be checked: {errormsg}")
