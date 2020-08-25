#!/usr/bin/python3

import os, sys, getopt, json
from configparser import ConfigParser

# We use this script's location to find our imports
def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(get_script_path() + "/..")

from tesla_api import TeslaApiClient
from tesla_api import AuthenticationError

def print_helptext():
    print("pw_setmode.py usage")
    print("-m {MODE} or --mode={MODE}")
    print("  - Operating mode - one of {backup, self_consumption, autonomous}")

def main(argv):
    newmode = ''
    try:
        opts, args = getopt.getopt(argv, "hm:", ["mode="])
    except getopt.GetoptError:
        print_helptext()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print_helptext()
            sys.exit(0)
        elif opt in ("-m", "--mode"):
            newmode = arg

    config = ConfigParser()
    configpath = get_script_path() + '/../etc/secrets.cfg'
    config.read(configpath)
    
    try:
        client = TeslaApiClient(config["api"]["email"], config["api"]["password"])

        energy_sites = client.list_energy_sites()
        assert(len(energy_sites)==1)
        if newmode == 'backup':
            energy_sites[0].set_operating_mode_backup()
            energy_sites[0].set_backup_reserve_percent(100)
        elif newmode == 'self_consumption':
            energy_sites[0].set_operating_mode_self_consumption()
            energy_sites[0].set_backup_reserve_percent(0)
        elif newmode == 'autonomous':
            energy_sites[0].set_operating_mode_autonomous()
            energy_sites[0].set_backup_reserve_percent(0)
        else:
            print("Invalid mode selected")
            sys.exit(2)
        sys.exit(0)
    except AuthenticationError as e:
        print("AuthenticationError: " + e)
        sys.exit(1)
    
if __name__ == "__main__":
    main(sys.argv[1:])
