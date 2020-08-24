#!/usr/bin/python3

import os
import sys
# This app looks for a folder called .env in the root to find tesla_api folder at that level
from dotenv import find_dotenv
sys.path.append(os.path.dirname(find_dotenv()))

from tesla_api import TeslaApiClient
from tesla_api import AuthenticationError
from configparser import ConfigParser
import json

def main():
    config = ConfigParser()
    configpath = os.path.dirname(find_dotenv()) + 'etc/secrets.cfg'
    print("Reading config from: " + configpath)
    config.read(configpath)
    print("Authenticating: " + config["api"]["email"])
    
    try:
      client = TeslaApiClient(config["api"]["email"], config["api"]["password"])
    
      energy_sites = client.list_energy_sites()
      assert(len(energy_sites)==1)
      print("Current operating mode: " + str(energy_sites[0].get_operating_mode()) + ", reserve: " +  str(energy_sites[0].get_backup_reserve_percent()))
      energy_sites[0].set_operating_mode_self_consumption()
      energy_sites[0].set_backup_reserve_percent(0)
      print("Now self consumption (0)")
    
      return 0
    except AuthenticationError as e:
      print("AuthenticationError: " + e)
      return 1
    
if __name__ == "__main__":
    main()

