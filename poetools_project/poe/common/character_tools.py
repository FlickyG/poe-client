#!/bin/python3
from django.core.urlresolvers import reverse 

import pprint
import poe.models

import logging
import time
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import DatabaseError,IntegrityError
from django.core.exceptions import MultipleObjectsReturned
import json
import re


from poe.models import ItemCategory, FixCategory, FixType, Fix, Stats 
from poe.models import StatNames, FixName, Stats, ItemName, ItemType, ItemStat
from poe.models import StatTranslation

stdlogger = logging.getLogger("poe_generic")
proj_path = '/Users/adam.green/Documents/workspace/poe-client/poetools_project/'

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

def contains_word(s, w):
    #stdlogger.info("string %s", s)
    #stdlogger.info("word %s", w)
    return (' ' + w + ' ') in (' ' + s + ' ')

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
    ggg_url = "https://www.pathofexile.com/character-window/get-characters"
    resp = s.get(ggg_url, cookies = {'POESESSID': poe_account.sessid})
    data = resp.json()
    live_charnames = set([line['name'] for line in data])
    # delete stale characters
    # in saved_charnames but not in live_charnames
    delete_chars = saved_charnames.difference(live_charnames)
    for char in saved_chars:
        if char.name in delete_chars: 
            stdlogger.info("character names that need to be deleted", char)
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
    stdlogger.info("== Registering Flicky ==")
    account = poe.models.PoeUser.objects.get(poe_account_name = "greenmasterflick")
    x = poe.models.PoeAccount(
                          acc_name = account.poe_account_name,
                          sessid = "df2fee550dae55266a9b48972e57ff7f",
                          )
    x.save()
    
def register_greenmasterflick():
    stdlogger.info("== Registering greenmasterflick ==")
    x = poe.models.PoeUser(
                           poe_account_name = "greenmasterflick"
                           )
    x.save()

def get_char_items(poe_account, character):
    """
    Downloads the items held in the characters slots and stash, retruns the
    equipped items 
    Accepts: the relevant account and character
    Returns: the equipment held by this character
    """
    stdlogger.info("getting character items")
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
    # check there's a proper session id
    try:
        assert len(poe_account.sessid) == 32
    except AssertionError as e:
        stdlogger.info("Try updating the session id")
        return(None)        
    league = "Standard"
    try:
        raise requests.exceptions.ConnectionError
        marketStatUrl = ("https://www.ppathofexile.com/character-window/get-stash-items?"
                        "league={lg}&tabs=1&tabIndex={ind}&"
                        "accountName={acc}".format(lg = league, ind = tabIndex,
                                                   acc = poe_account.acc_name))
        resp = s.get(marketStatUrl, cookies = {'POESESSID': poe_account.sessid})
        tab_data = resp.json()
        tab_items = tab_data['items']
    except requests.exceptions.ConnectionError:
        stdlogger.info("URL Connection Error Attempting to load from file")
        try:
            data_file = "poe/data/tab_data/data_"+str(tabIndex)
            with open(data_file, 'r') as file:
                all_data = json.load(file)
                tab_items = all_data['items']
                stdlogger.info("Loading from file success")
        except FileNotFoundError:
            stdlogger.info("file not found %s", data_file)
            return(None)
    for each_item in tab_items:
        #stdlogger.info("name %s, type line %s", each_item["name"], each_item["typeLine"])
        if contains_word( each_item["typeLine"], "Map"):
            stdlogger.info("Map Found")
        elif contains_word(each_item["typeLine"], "Leaguestone"):
            stdlogger.info("Leaguestone Found")
        elif contains_word(each_item["typeLine"], "Flask"): 
            stdlogger.info("Flask Found")
        else:
            parse_items(each_item, poe_account, tabIndex)
        
        
def parse_items(each_item, poe_account, tab_index):
#print("name = ", each_item['typeLine'])
    if 'properties' in each_item.keys():
        for each_prop in each_item['properties']:
            stdlogger.debug("each_prop %s", each_prop)
    # calculate requirements
    if 'requirements' in each_item.keys():
        for each_req in each_item['requirements']:
            # lvl
            if 'Level' in each_req.values():
                rlvl = each_req['values'][0][0]
            else:
                rlvl = 0
            # str
            if 'Str' in each_req.values():
                rstr = each_req['values'][0][0]
            else:
                rstr = 0
            # int
            if 'Int' in each_req.values():
                rint = each_req['values'][0][0]
            else:
                rint = 0
            # dex
            if 'Dex' in each_req.values():
                rdex = each_req['values'][0][0]
            else:
                rdex = 0
    else: # no requirements
        rlvl = rstr = rint = rdex = 0
    # check the new type field already exists in the database        # need to add other item categories e.g. gems, maps
    # then need to add item type, 
    # if superior, remove from nam
    stdlogger.debug("item is %s", each_item)
    stdlogger.debug("item name is %s", each_item['name'])
    # White superior items
    if contains_word(each_item["typeLine"], "Superior"):
        item_name = each_item["typeLine"].split(' ', 1)[1]
        base_name = item_name
        stdlogger.debug("item_name contains superior")
        rarity = "normal"
    # Magic items
    elif len(each_item['name']) == 0 and '<<set' in each_item["typeLine"]:
        try:
            base_name = each_item["typeLine"].split('<<set:MS>><<set:M>><<set:S>>',1)[1]
            item_name = base_name
            rarity = "magic"
        except IndexError as e:
            stdlogger.info("The index of base_name didn't work when trying to" 
                           "parse a magic item %s", each_item["typeLine"])
        for i in range(0,len(base_name.split()) - 1):
            stdlogger.info("i %s %s", i, base_name)
            try:
                lookup = base_name.split()[i] + " " + base_name.split()[i+1]
            except AttributeError as e:
                stdlogger.info("Attribute Error lookup %s", lookup)
            try:
                base_name = poe.models.ItemName.objects.get(name = lookup)
                break
            except ObjectDoesNotExist as e:
                stdlogger.info("magic base name not found, as expected, %s", lookup)
    # Rare Items pt 1 of 2
    elif len(each_item['name']) == 0 and '<<set' not in each_item["typeLine"]:
        item_name = each_item["typeLine"]
        base_name = item_name
        rarity = "rare"
    # Rare items pt 2 of 2
    else:
        item_name = each_item['name'].split('<<set:MS>><<set:M>><<set:S>>',1)[1]
        base_name = each_item['typeLine']
        rarity = "rare"
    try:
        the_base_type = poe.models.ItemName.objects.get(name = base_name)
    except ObjectDoesNotExist as e:
        the_base_type = None
        stdlogger.info("item not found base_name = %s item_name = %s", base_name, item_name)
        if base_name == "<<set:MS>><<set:M>><<set:S>>Robust Lapis Amulet of the Thunderhead":
            print("HELLO !!!!!!!!")
            pprint.pprint(each_item)
            return(each_item)
    # Quality
    """ 'properties': [{'displayMode': 0,
             'name': 'Quality',
             'type': 6,
             'values': [['+10%', 1]]},
            {'displayMode': 0,
             'name': 'Chance to Block',
             'type': 15,
             'values': [['25%', 0]]},
            {'displayMode': 0,
             'name': 'Evasion Rating',
             'type': 17,
             'values': [['217', 1]]}],
    """
    if 'properties' in each_item:
        for each_property in each_item['properties']:
            if each_property['name'] == "Quality":
                #stdlogger.info("quality item detected %s", each_property["values"][0][0].strip('+%'))
                the_quality =  each_property["values"][0][0].strip('+%')
                break
            else:
                #stdlogger.info("quality detected but setting to 0")
                the_quality = 0
    else:
        #stdlogger.info("no quality detected")
        the_quality = 0
    # Parse Mods
    """
    +9 to Dexterity
    +29 to Intelligence
    10% increased Evasion and Energy Shield
    +19 to maximum Energy Shield
    7% increased Stun and Block Recovery
    +19 to maximum Energy Shield
    +27% to Fire Resistance
    32% increased Stun Duration on Enemies
    24% increased Stun and Block Recovery
    Adds 1 to 2 Physical Damage to Attacks
    """
    if 'explicitMods' in each_item:
        for each_mod in each_item['explicitMods']:
            original_mod = each_mod
            # replace all +, % and numbers
            numbers = "0123456789"
            for n in numbers:
                if n in each_mod:
                    each_mod = each_mod.replace(n, '#')
            each_mod = re.sub('#+','#', each_mod) # remove duplicates
            # handle decimals
            each_mod = each_mod.replace("#.#%", "#%")
            #also need a new function to modify the translations file
            '''if '+%' in each_mod:
                stdlogger.info("plus percent in each_mod %s", each_mod)
                #each_mod = each_mod.replace('+%', '+')
                #use the format entry in the stat translations file to work out if it should be +
                #for physical damage or +% for resistances
                pass
            elif '%' in each_mod:
                each_mod = each_mod.replace('%', '+%')
            ''' 
            try:
                database_lookup = poe.models.StatTranslation.objects.get(name = each_mod)
                stdlogger.debug("And here is the databse lookup %s", database_lookup)
            except ObjectDoesNotExist as e:
                stdlogger.info("==")
                stdlogger.info("Here is an explicitMod %s", original_mod)
                stdlogger.info("This mod wasn't found ObjectDoesNotExist %s", each_mod)
            except ValueError as e:
                stdlogger.info("==")
                stdlogger.info("Here is an explicitMod %s", original_mod)
                stdlogger.info("Value Error %s", each_mod)
            except IndexError as e:
                stdlogger.info("==")
                stdlogger.info("Here is an explicitMod %s", original_mod)
                stdlogger.info("IndexError %s", each_mod)
            except MultipleObjectsReturned as e:
                pass
                #stdlogger.info("==")
                #stdlogger.info("Here is an explicitMod %s", original_mod)
                #stdlogger.info("Multiple Objects Returned %s", each_mod)
    # Save Item
    try:
        entry = poe.models.PoeItem(
                    base_type = the_base_type,
                    #name = (poe.models.ItemName.objects
                    #ß        .get(name = each_item['typeLine'])), #change this to type and link to ItemName.name
                    #add a name e.g. Grim Skewer which is taken from name': '<<set:MS>><<set:M>><<set:S>>Grim Skewer',
                    name = item_name,
                    owner = poe_account,
                    ggg_id = each_item['id'],
                    ilvl = each_item['ilvl'],
                    tab_location = tab_index,
                    equipped = False,
                    char_stash = False,
                    x_location = each_item['x'],
                    y_location = each_item['y'],
                    raw_data = each_item,
                    req_lvl = rlvl,
                    req_str = rstr,
                    req_int = rint,
                    req_dex = rdex,
                    rarity = rarity,
                    quality = the_quality,
                    )
        #add a free text field and save the dictionary for each item, for the time being.  It will help debug later
        #items also need owners
        #add logic to save all items in all tabs
        #add logic to create new items type, and types generally
        entry.save()
    except IntegrityError as e:
        stdlogger.debug("duplicate entry %s", each_item['typeLine'])
#return tab_items
    
def get_tab_details(poe_account):
    """
    Fetches from GGG the details of the users stash tabs (but not their contents)
    This data includes the tab names, unique ID, player index, colour, etc.
    Accepts: The account and character - do we need the character, can't we pick
            one and remove this constraint when calling the function?
    Returns: a list of dictionaries, one list item per tab
    """
    stdlogger.info("getting items")
    league = "Standard"
    marketStatUrl = ("https://www.pathofexile.com/character-window/get-stash-items?"
                    "league={lg}&tabs=1&tabIndex={ind}&"
                    "accountName={acc}".format(lg = league, ind = 0,
                                               acc = poe_account.acc_name))
    resp = s.get(marketStatUrl, cookies = {'POESESSID': poe_account.sessid})
    stash_items = resp.json()
    # y['tabs'][0].keys()
    # dict_keys(['selected', 'srcL', 'n', 'id', 'hidden', 'srcC', 'srcR', 
    # 'colour', 'type', 'i'])
    for each_tab in stash_items['tabs']:
            tab_details = poe.models.PoeTab(
                              index = each_tab['i'], 
                              ggg_identifier = each_tab['id'], 
                              name = each_tab['n'],
                              owner = poe_account,
                              )
            tab_details.save()
    return poe.models.PoeTab.objects.filter(owner = poe_account)

def delete_all_users_tabs(poe_account):
    """
    Deletes all entries in the tab table for the account given
    """
    tab_details = poe.models.PoeTab.objects.filter(owner = poe_account)
    for each_tab in tab_details:
        each_tab.delete()

def delete_all_tabs():
    """
    Deletes all entries in the tab table
    """
    tab_details = poe.models.PoeTab.objects.all()
    for each_tab in tab_details:
        each_tab.delete()
        
def delete_all_user_items(poe_account):
    """
    Deletes all entries in the item table for the account given
    """
    all_user_items = poe.models.PoeItem.objects.filter(owner = poe_account)
    for item in all_user_items:
        item.delete()

def delete_all_items():
    """
    Deletes all entries in the item table
    """
    all_items = poe.models.PoeItem.objects.all()
    for each_item in all_items:
        each_item.delete()
        
def load_item_data_from_file(file):
    """
    Accepts: a json file
    Returns: None
    """
    stdlogger.info("no code here yet when trying to add items from file")

def get_location(id):
    the_item = poe.models.PoeItem.objects.get(ggg_id = id)
    return (the_item.location)

def get_item_name(id):
    """
    Accepts:    The numerical ID of the item of interest where these items are
                those stored in people's inventory                
    Returns:    The name of the item, e.g. "Rift Scratch"
    """
    the_item = poe.models.PoeItem.objects.get(ggg_id = id)
    return (the_item.name)



def get_tab_items_file(poe_account, tabIndex):
    """
    Fetches from the website the contents of an account's stash tab
    Accepts: the account details
             the tab index of interest
    Returns: the json for the API request
    """
    # check there's a proper session id
    x = 0
    while x < 50:
        try:
            assert len(poe_account.sessid) == 32
        except AssertionError as e:
            stdlogger.info("Try updating the session id")
            return(None)        
        league = "Standard"
        marketStatUrl = ("https://www.pathofexile.com/character-window/get-stash-items?"
                        "league={lg}&tabs=1&tabIndex={ind}&"
                        "accountName={acc}".format(lg = league, ind = x,
                                                   acc = poe_account.acc_name))
        resp = s.get(marketStatUrl, cookies = {'POESESSID': poe_account.sessid})
        tab_data = resp.json()
        file = "data_"+str(x)
        with open(file, 'w') as outfile:
            json.dump(tab_data, outfile)
        x = x+1

def print_stat_trans():
    proj_path = '/Users/adam.green/Documents/workspace/poe-client/poetools_project/'
    data_path = proj_path+"poe/data/"
    df = open(data_path+"stat_translations.json").read()
    a = json.loads(df)
    for x in a:
        database_string = x['ids'][0]
        stdlogger.info("Loading from file success")     

def load_stat_translations():
    #Load the RePoe JSON File
    data_path = proj_path+"poe/data/"
    df = open(data_path+"stat_translations.json").read()
    a = json.loads(df)
    # scrape the file and add the model entries
    for x in a:
        # data base string is the 'id' field in RePoe's file and needs a bit of regex to format it into the same as the GGG webpage
        database_string = str(x["ids"][0])
        #stdlogger.debug("database_string %s", database_string)
        database_string = (database_string).title().replace('_', ' ')  
        if len(x["ids"]) == 1:
            # in case there are more than one mapping
            for y in range(0, len(x["English"])):
                # download_string is the string appended to the item in the api download from ggg
                the_f = str(x["English"][y]["format"][0])
                download_string = str(x["English"][y]["string"]).replace('{0}',the_f)
                #download_string = download_string.replace('{1}',the_f)
                try:
                    database_version = StatNames.objects.get(name = database_string)
                    stdlogger.debug("success %s %s", database_string, download_string)
                    # save mapping
                    mapping = StatTranslation.objects.get_or_create(
                                name = download_string,
                                web_name = database_version
                                )
                    #mapping.save()
                except StatNames.DoesNotExist:
                    stdlogger.info("StatNames.DoesNotExist %s", database_string) # not expecting all lookups to work
                except Exception:
                    stdlogger.info("something else went wrong")
        if len(x["ids"]) == 2:
            stdlogger.info("length of ids is 2")
            for y in range(0,2):
                # download_string is the string appended to the item in the api download from ggg
                the_f = str(x["English"][0]["format"][y])
                index_string = ''.join(['{',str(y),'}'])
                #stdlogger.info("raw download_string %s", str(x["English"][0]["string"]))
                #stdlogger.info("index_string %s", index_string)
                download_string = str(x["English"][0]["string"]) #.replace(index_string,the_f)
                download_string = download_string.replace('{0}',the_f)
                download_string = download_string.replace('{1}',the_f)
                #stdlogger.info("download_string %s", download_string)
                # database string is the equivalent version on the poe/items page
                database_string = str(x["ids"][y])
                database_string = (database_string).title().replace('_', ' ')
                stdlogger.info("NEW database_string %s", database_string)
                try:
                    database_version = StatNames.objects.get(name = database_string)
                    #stdlogger.info("success %s %s", database_string, download_string)
                    # save mapping
                    mapping = StatTranslation.objects.get_or_create(
                                name = download_string,
                                web_name = database_version
                                )
                    #mapping.save()
                except StatNames.DoesNotExist:
                    stdlogger.info("StatNames.DoesNotExist %s", database_string) # not expecting all lookups to work
                except Exception:
                    stdlogger.info("something else went wrong")
        if len(x["ids"]) > 2:
            # ['bleed_on_hit_with_attacks_%', 'global_bleed_on_hit', 'cannot_cause_bleeding']
            # ['unique_chaos_damage_to_reflect_to_self_on_attack_%_chance', 'unique_minimum_chaos_damage_to_reflect_to_self_on_attack', 'unique_maximum_chaos_damage_to_reflect_to_self_on_attack']
            # ['map_fishy_effect_0', 'map_fishy_effect_1', 'map_fishy_effect_2', 'map_fishy_effect_3']
            stdlogger.info("length of ids is greater than 2 %s", str(x["ids"]))

def delete_stat_translations():
    """ Deletes all entrires in the stat translation table """
    data = poe.models.StatTranslation.objects.all()
    for d in data:
        d.delete()


#trans = poe.models.StatTranslation.objects.all()
#for x in trans:
#    x.delete() 

"""
import pprint
import poe.common.character_tools
import poe.models
import ast # enable conversion of string to dictionary

poe.common.character_tools.delete_stat_translations()
poe.common.character_tools.load_stat_translations()

poe.common.character_tools.register_flicky()
account = poe.models.PoeAccount.objects.get(acc_name = 'greenmasterflick')
x = poe.common.character_tools.get_tab_items(account, 15)

stash_tab_items = poe.common.character_tools.get_tab_items(account, 2)


{'corrupted': False,
 'explicitMods': ['+53 to maximum Life', '+26% to Lightning Resistance'],
 'frameType': 1,
 'h': 1,
 'icon': 'https://web.poecdn.com/image/Art/2DItems/Amulets/Amulet5.png?scale=1&scaleIndex=0&w=1&h=1&v=574b38016f547495a51268177882d5cc3',
 'id': 'ddde9268a97d2fe7d254f647eb35c5209aa9846c047cb0f659bff5ffef7da663',
 'identified': True,
 'ilvl': 53,
 'implicitMods': ['+21 to Intelligence'],
 'inventoryId': 'Stash16',
 'league': 'Standard',
 'lockedToCharacter': False,
 'name': '',
 'requirements': [{'displayMode': 0, 'name': 'Level', 'values': [['29', 0]]}],
 'socketedItems': [],
 'sockets': [],
 'typeLine': '<<set:MS>><<set:M>><<set:S>>Robust Lapis Amulet of the '
             'Thunderhead',
 'verified': False,
 'w': 1,
 'x': 9,
 'y': 4}

## parse items

for item in stat_tab_items:
    item_type = poe.models.ItemType.object.get(name = item['typeline']|)
    name_str = item['name'].split('<<set:MS>><<set:M>><<set:S>>',1)[1],
    #name = poe.models.ItemType.objects.get(name = name_str)
    name = name_str #models.CharField(max_length = 264, blank = False, ) 
    owner = models.ForeignKey(PoeAccount) 
    ggg_id = item['id']
    raw_data = item
    ilvl = item['ilvl']
    tab_location = models.IntegerField()
    x_location = item['x']
    y_location = item['y']
    w_location = item['w']
    for req in requirements:
        if req['name'] == "Level":
            req_lvl = req['values'][0][0]
        elif if req['name'] == "Str":
            req_lvl = req['values'][0][0]
        elif if req['name'] == "Int":
            req_lvl = req['values'][0][0]
        elif if req['name'] == "Dex":
            req_lvl = req['values'][0][0]
        else:
            print("unknown requirement! Exiting . . . ")
            sys.exit(0)
    this_item = poe.models.PoeItem(
                item_type = 


poe.common.character_tools.get_characters(account)
poe.common.character_tools.get_tab_details(account)
char = poe.models.PoeCharacter.objects.get(name = 'LetsGetPhysicalRanger')
data =  poe.common.character_tools.get_char_items(account, char)

equiped_items = data['items']

stash_tab_items = poe.common.character_tools.get_tab_items(account, 1)

== print properties
currency_mods = ['Stack Size']
map_mods = [ 'Map Tier',
            'Item Quantity',
            'Monster Pack Size',
            ]
items_unknown = []
my_items = poe.models.PoeItem.objects.all()
for item in my_items:
    data = ast.literal_eval(item.raw_data)
    if 'properties' in data.keys():
        for property in data['properties']:
            x = poe.models.StatNames.objects.filter(name__search = property['name'])
            if not x and property['name'] not in map_mods and property['name'] not in currency_mods:
                items_unknown.append(item)
                print("x was not found", property['name'])
            elif x:
                print("x was found", x[0].name, item.name)
            else:
                print("weird else clause")
    if 'explicitMods' in data.keys():
        for mod in data['explicitMods']:
            print(mod)

=== print requirements
for x in all_items:
    b = ast.literal_eval(x.raw_data)
    if 'requirements' in b.keys():
            print(b['requirements'])
==

for x in all_items:
    b = ast.literal_eval(x.raw_data)
    if 'requirements' in b.keys():
            print(b['requirements'])

===

#>>> the_tab_items[1].keys()
#dict_keys(['ilvl', 'icon', 'lockedToCharacter', 'properties', 'h', 'id', 'name', 'w', 'sockets', 'identified', 'verified', 'descrText', 'inventoryId', 'corrupted', 'frameType', 'x', 'league', 'socketedItems', 'y', 'typeLine'])


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



