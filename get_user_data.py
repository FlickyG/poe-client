#!/bin/python3
# stuff
import requests, requests_cache, json
import datetime, time, pprint
from pip._vendor.distlib import database
## for sql
import psycopg2
import logging
from xml.dom.pulldom import CHARACTERS

#this needs to be replaced with the value passed by the django login screen
USER = "adam"
SESSID = "4f81b66c24e87dda9dded625035ee4e5"

url_characters = "www.pathofexile.com/character-window/get-characters"


logging.config.fileConfig('poe_tools_logging.conf')
logger = logging.getLogger(__name__)
start_time = datetime.datetime.now()
logger.info("Staring POE Tools at "+str(start_time))
print(__name__)

def make_throttle_hook(timeout=1.0):  # for eve market api calls
    """
    Returns a response hook function which sleeps for `timeout` seconds if
    response is not cached
    """
    def hook(response, **kwargs):
        if not getattr(response, 'from_cache', False):
            #print ('sleeping')
            time.sleep(timeout)
        return response
    return hook


requests_cache.install_cache('first_go', expires_after = 1)
requests_cache.clear()
s =  requests.Session()
s.hooks = {'response': make_throttle_hook(0.1)}


url_characters = "www.pathofexile.com/character-window/get-characters"

#get account details from data base
marketStatUrl = "https://www.pathofexile.com/character-window/get-characters"
characters = s.get(marketStatUrl, cookies = {'POESESSID': SESSID}).json
print(characters)

for character in characters:
    print(character)



#fetch character names for each account and dump into data base
#fetch tab names and ids for each account and dump into data base
#for each tab, fetch items in tab
#for each item, store in data base
