#!/usr/bin/python3

import os
import sys
def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

sys.path.append(get_script_path() + "/..")

from tesla_api import TeslaApiClient
from tesla_api import AuthenticationError
from configparser import ConfigParser
import json

def main():
    config = ConfigParser()
    configpath = get_script_path() + '/../etc/secrets.cfg'
    config.read(configpath)
    
    try:
      client = TeslaApiClient(config["api"]["email"], config["api"]["password"])
    
      energy_sites = client.list_energy_sites()
      assert(len(energy_sites)==1)
      print(energy_sites[0].get_operating_mode())
      
      return 0
    except AuthenticationError as e:
      print("AuthenticationError: " + e)
      return 1
    
if __name__ == "__main__":
    main()

