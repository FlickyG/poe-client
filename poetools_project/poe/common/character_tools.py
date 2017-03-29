#!/bin/python3
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
    stdlogger.debug("hello from get_characters")
    print("hello world 2", poe_account.acc_name, poe_account.sessid)
    # grab current character names from daabase
    saved_chars = poe.models.PoeCharacter.objects.all()
    saved_charnames = set([char.name for char in saved_chars])
    print("saved.charnames", saved_charnames)
    #get character names on the server right now
    ggg_url = "https://www.pathofexile.com/character-window/get-characters"
    resp = s.get(ggg_url, cookies = {'POESESSID': poe_account.sessid})
    data = resp.json()
    live_charnames = set([line['name'] for line in data])
    print("live_charnames", live_charnames)
    live_subs_saved = live_charnames.issubset(saved_charnames)
    saved_subs_live = saved_charnames.issubset(live_charnames)
    # delete stale characters
    # in saved_charnames but not in live_charnames
    x = saved_charnames.difference(live_charnames)
    print("x", x)
    # insert new characters
    # in live_charnames but not in saved_charnames
    add_chars = live_charnames.difference(saved_charnames)
    for char in add_chars:
        print("char", char)
    pass