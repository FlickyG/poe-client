#!/bin/python3
from django.core.urlresolvers import reverse 


import poe.models

import logging
import time
import requests
stdlogger = logging.getLogger("poe_generic")

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

s =  requests.Session()
s.hooks = {'response': make_throttle_hook(0.1)}


def get_characters(poe_account):
    stdlogger.debug("entering get_characters")
    # grab current character names from daabase
    saved_chars = poe.models.PoeCharacter.objects.all()
    saved_charnames = set([char.name for char in saved_chars])
    #get character names on the server right now
    ggg_url = "https://www.pathofexile.com/character-window/get-characters"
    resp = s.get(ggg_url, cookies = {'POESESSID': poe_account.sessid})
    data = resp.json()
    live_charnames = set([line['name'] for line in data])
    # delete stale characters
    # in saved_charnames but not in live_charnames
    delete_chars = saved_charnames.difference(live_charnames)
    for char in saved_chars:
        if char.name in delete_chars: 
            print("character names that need to be deleted", char)
            char.delete()
    # insert new characters
    # in live_charnames but not in saved_charnames
    add_chars = live_charnames.difference(saved_charnames)
    for char in data:
        if char['name'] in add_chars:
            stdlogger.debug(' '.join(("Need to create this character", char['name'])))
            new_char = poe.models.PoeCharacter(
                        account = poe_account,
                        name =char['name'],
                        level = char['level'],
                        ggg_class = char['class'],
                        ascendancy_class = char['ascendancyClass'],
                        classId = char['classId'],
                        league = char['league'], 
                        )
            new_char.save()

def delete_all_characters():
    all_chars = poe.models.PoeCharacter.objects.all()
    for char in all_chars:
        stdlogger.debug(' '.join(("Deleting this character", char.name)))
        char.delete()
        
def register_flicky():
    account = poe.models.PoeAccount.get(acc_name = "flickyg")
    

def get_items(poe_account, character):
    print("hello")
    equiped_items_URL = ("http://www.pathofexile.com/character-window/get-items?"
                     "character={char}&accountName={acc}"
                     .format(char = character.name, acc = poe_account.acc_name))
    resp = s.get(equiped_items_URL, cookies = {'POESESSID': poe_account.sessid})
    equipment = resp.json()
    return equipment

