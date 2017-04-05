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
    """
    Downloads all Character infor from the API end point and saves this data 
    to the database  
    """
    stdlogger.debug("entering get_characters")
    # grab current character names from daabase
    saved_chars = poe.models.PoeCharacter.objects.all()
    saved_charnames = set([char.name for char in saved_chars])
    #get character names on the server right now
    2
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
    """
    Crudely deletes all characters from the table
    """
    all_chars = poe.models.PoeCharacter.objects.all()
    for char in all_chars:
        stdlogger.debug(' '.join(("Deleting this character", char.name)))
        char.delete()
        
def register_flicky():
    """
    Useful tool to reinstate my own account after wiping the psql database
    """
    account = poe.models.PoeAccount.get(acc_name = "flickyg")
    

def get_char_items(poe_account, character):
    """
    Downloads the items held in the characters slots and stash, retruns the
    equipped items 
    Accepts: the relevant account and character
    Returns: the equipment held by this character
    """
    print("getting character items")
    equiped_items_URL = ("http://www.pathofexile.com/character-window/get-items?"
                     "character={char}&accountName={acc}"
                     .format(char = character.name, acc = poe_account.acc_name))
    resp = s.get(equiped_items_URL, cookies = {'POESESSID': poe_account.sessid})
    equipment = resp.json()
    return equipment

def get_tab_items(poe_account, tabIndex):
    """
    Fetches from the website the contents of an account's stash tab
    Accepts: the account details
             the tab index of interest
    Returns: the json for the API request
    """
    print("getting items")
    league = "Legacy"
    marketStatUrl = ("https://www.pathofexile.com/character-window/get-stash-items?"
                    "league={lg}&tabs=1&tabIndex={ind}&"
                    "accountName={acc}".format(lg = league, ind = tabIndex,
                                               acc = poe_account.acc_name))
    resp = s.get(marketStatUrl, cookies = {'POESESSID': poe_account.sessid})
    stash_items = resp.json()
    return stash_items
    
def get_tab_details(poe_account, character):
    """
    Fetches from GGG the details of the users stash tabs (but not their contents)
    This data includes the tab names, unique ID, player index, colour, etc.
    Accepts: The account and character - do we need the character, can't we pick
            one and remove this constraint when calling the function?
    Returns: a list of dictionaries, one list item per tab
    """
    print("getting items")
    league = "Legacy"
    marketStatUrl = ("https://www.pathofexile.com/character-window/get-stash-items?"
                    "league={lg}&tabs=1&tabIndex={ind}&"
                    "accountName={acc}".format(lg = league, ind = 0,
                                               acc = poe_account.acc_name))
    resp = s.get(marketStatUrl, cookies = {'POESESSID': poe_account.sessid})
    stash_items = resp.json()
    # y['tabs'][0].keys()
    # dict_keys(['selected', 'srcL', 'n', 'id', 'hidden', 'srcC', 'srcR', 'colour', 'type', 'i'])
    return stash_items['tabs']

"""
import poe.models
import poe.common.character_tools

account = poe.models.PoeAccount.objects.get(acc_name = 'greenmasterflick')
poe.common.character_tools.get_characters(account)
char = poe.models.PoeCharacter.objects.get(name = 'LetsGetPhysicalRanger')
data =  poe.common.character_tools.get_char_items(account, char)

ggg_items = data['items']

the_tabs = poe.common.character_tools.get_tab_details(account, char)
#the_tabs[0].keys()
#dict_keys(['colour', 'selected', 'srcL', 'id', 'n', 'srcR', 'hidden', 'srcC', 'i', 'type'])

y = poe.common.character_tools.get_tab_items(account, 0, char)

y = poe.common.character_tools.get_tab_items(account, 5, char)

"""
""" getting items

pprint.pprint(y['items'][7])

{'corrupted': False,
 'explicitMods': ['+1 to Level of Socketed Lightning Gems',
                  '30% increased Critical Strike Chance for Spells',
                  '+28% to Fire Resistance',
                  '+6% Chance to Block'],
 'frameType': 2,
 'h': 2,
 'icon': 'https://web.poecdn.com/image/Art/2DItems/Armours/Shields/ShieldInt6.png?scale=1&w=2&h=2&v=c2c4daefcbef51dad8593cf61505a1933',
 'id': '9dcc6d7a4785aeeb45ad50eee4d37bcad4c1143ac83da59f2d4954f663bdb428',
 'identified': True,
 'ilvl': 72,
 'inventoryId': 'Stash6',
 'league': 'Legacy',
 'lockedToCharacter': False,
 'name': '<<set:MS>><<set:M>><<set:S>>Dread Wish',
 'properties': [{'displayMode': 0,
                 'name': 'Chance to Block',
                 'type': 15,
                 'values': [['31%', 1]]},
                {'displayMode': 0,
                 'name': 'Energy Shield',
                 'type': 18,
                 'values': [['84', 0]]}],
 'requirements': [{'displayMode': 0, 'name': 'Level', 'values': [['68', 0]]},
                  {'displayMode': 1, 'name': 'Int', 'values': [['159', 0]]}],
 'socketedItems': [],
 'sockets': [{'attr': 'I', 'group': 0},
             {'attr': 'I', 'group': 0},
             {'attr': 'I', 'group': 1}],
 'typeLine': 'Titanium Spirit Shield',
 'verified': False,
 'w': 2,
 'x': 8,
 'y': 4}
"""


