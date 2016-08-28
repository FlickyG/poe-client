#!/bin/python3
# stuff
import sqlite3, requests, requests_cache, json
import time, pprint
from pip._vendor.distlib import database
## for sql
import psycopg2

#my specific globals
#TABS = []
CHARACTERS= []
ACCOUNTS = []
ACCOUNT_NAME = ""
SESSID = []


cookie = {'poesessid': '4f81b66c24e87dda9dded625035ee4e5'}



CHARACTERS = []

class db_queries(object):
    """ Handles SQL calls to the Eve Online SDE held locally on this machine.
        You may need to repoint the location of the sqlite3.connect statement
        TDO - error hanfdling on this and option for CLI input
    """
    #self.logging.basicConfig(filename='eve-EVEMarkets.log',level=logging.DEBUG)
    
    def __init__(self):
        try:
            conn = psycopg2.connect("dbname='poe_data' user='adam'")
            print("connected to the database")
        except Exception as inst:
            print("I am unable to connect to the database", inst)
            
         
class poe_tab(object):
    def __init__(self, data, account_name):
        self.id = data['i']
        self.name = data['n']
        self.owner = account_name
        self.colour = data['colour']
    

class poe_character(object):
    def __init__(self, character):
        self.name = character['name']
        self.classID = character['classId']
        self.classs = character['class']
        self.league = character['league']
        self.level = character['level']
        self.ascendancy_class = character['ascendancyClass']
        
        

class poe_properties(object):
    def __init__(self, data):
        self.id = None
        self.name = data['name']
        self.value1 = data['values'][0]
        self.value2 = data['values'][1]

class poe_item(object):
    def __init__init(self, data):
        self.id = None # comes from db
        self.name = data['typeLine']
        self.gggid = data['id']
        ilvl = data['ilvl']
        self.owner = None # comes from db
        self.properties = poe_properties(data['properties'])
        self.w = data['w']
        self.x  = data['x']
        self.y = data['y']

class character(object):
    def __init__(self, data):
        self.id = None #comes from db
        self.account_name = None # not sure how to get this in
        self.name = data

class account(object):
    def __init__(self, data):
        self.id = None #coimes from db
        self.account_name = data
        

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

#setup HTTP session
#monkey patch requests_cache


def  get_equiped_items(values, characters, account_name):
    #only works for active character!  Nedd try /except block , assert equipmernt = true
    #get equiped items
    marketStatUrl = ("http://www.pathofexile.com/character-window/get-items?"
                     "character={char}&accountName={acc}"
                     .format(char = characters.name, acc = account_name))
    resp = s.get(marketStatUrl, cookies = {'POESESSID': values})
    equipment = resp.json()
    #print (equipment)
    #find items without properties = jewelary and quest items
    y = 0
    for x in equipment['items']:
        try:
            if x['properties']:
                pass
                #print (x['typeLine'])
                #pprint.pprint(x['properties'])
        except KeyError as e:
            print (y, x['typeLine'])
        y = y+1
    
#get stash items

def get_stash_items(sessid, tabIndex, the_account):
    '''
    Returns the items in the required stash tab 
    '''
    league = "Standard"

    marketStatUrl = ("https://www.pathofexile.com/character-window/get-stash-items?"
                    "league={lg}&tabs=1&tabIndex={ind}&"
                    "accountName={acc}".format(lg = league, ind = tabIndex,
                                               acc = the_account.account_name))
    resp = s.get(marketStatUrl, cookies = {'POESESSID': sessid})
    stash_items = resp.json()
    return stash_items
    
def get_tab_numbers_and_names(data):
    #get tab numbers and names
    for x in data['tabs']:
        print (x['i'],x['n'])

      
def get_tabs(sessid, the_account):
    TABS = []
    print(sessid, the_account)
    for x in get_stash_items(sessid, 0, the_account)['tabs']:
        TABS.append(poe_tab(x, the_account.account_name))
    return TABS

def print_items_in_tabs(data):
    #get items in this tab
    for x in data['items']:
        pprint.pprint(x)


#get_tab_numbers_and_names(x)

def print_tab_items(index):
    x = get_stash_items(index)
    for items in x['items']:
        id = items['id']
        typeLine = items['typeLine']
        try:
            properties = items['properties']
            #pprint.pprint(properties)
            #print(id, typeLine, properties)
        except KeyError as e:
            print (items['typeLine'], 'has no props')
        #print(id, typeLine, properties)
        #the_properties = items['properties']
        #pprint.pprint(id, typeLine)


def print_tabs():
    for x in get_stash_items(0)['tabs']:
        print (x['id'], x['n'], x['colour'])




requests_cache.install_cache('first_go', expires_after = 1)
requests_cache.clear()
s =  requests.Session()
s.hooks = {'response': make_throttle_hook(0.1)}
# set session cookie


COOKIES = {'greenmasterflick': '4f81b66c24e87dda9dded625035ee4e5'}



def scrape_data():
    for keys, values in COOKIES.items():
        marketStatUrl = "https://www.pathofexile.com/character-window/get-account-name"
        #print("values", values)
        resp = s.get(marketStatUrl, cookies = {'POESESSID': values})
        account_name = resp.json()
        print("accounts Names!", account_name)
        for key, value in account_name.items():
            print("print account!", key, value)
            ACCOUNTS.append(account(value))

#get account name
def scrape_all_data():
    for keys, values in COOKIES.items():
        print(keys, values)
        marketStatUrl = "https://www.pathofexile.com/character-window/get-account-name"
        #print("values", values)
        resp = s.get(marketStatUrl, cookies = {'POESESSID': values})
        account_name = resp.json()
        print("accounts Names!", account_name)
        for key, value in account_name.items():
            print("print account!", key, value)
            ACCOUNTS.append(account(value))
        for accounts in ACCOUNTS:
            print ("values and stuff", values, 0, accounts)
            #get tabs
            print(accounts.account_name)
            tabs = get_tabs(values, accounts)
            for tab in tabs:
                #get stash items
                time.sleep(1)
                x = get_stash_items(values, tab.id, accounts)
                for item in x["items"]:
                    pprint.pprint(item["typeLine"])
            #get character names
            marketStatUrl = "https://www.pathofexile.com/character-window/get-characters"
            resp = s.get(marketStatUrl, cookies = {'POESESSID': values})
            for the_characters in resp.json():
                pass
                #CHARACTERS.append(poe_character(the_characters))
                #print("the_characters", the_characters)
            for the_character in CHARACTERS:
                pass #get_equiped_items(values, the_character, accounts.account_name)

#ACCOUNTS[0].account_name          
#ACCOUNTS[0].id

def items_in_tab(tab_number):
    ITEMS = []
    items = get_stash_items(COOKIES[ACCOUNTS[0].account_name], tab_number, ACCOUNTS[0])
    for item in items["items"]:
        ITEMS.append(item)
        for item in ITEMS:
            print(item["name"], "|", item["typeLine"])
            pprint.pprint(item)
    return ITEMS


scrape_data()            
x = get_tabs(COOKIES[ACCOUNTS[0].account_name], ACCOUNTS[0])
for y in x:
    print (y.id, "|", y.name)
some_items = items_in_tab(17)
for items in some_items:
    if 'descrText' in items:
        # currecy, gems, cards
        print(items['typeLine'])


for items in some_items:
    if items['ilvl'] == 0: #currency,  cards, gems
        if 'secDescrText' in items: #gems
            pass
            #print(items['typeLine'])
            #pprint.pprint(items)
        else:
            pass
    elif items['ilvl'] > 0:
        if 'Amulet' in items['typeLine'] or 'Ring' in items['typeLine']:
            pass
        elif (items['typeLine'] and items['name']):
            #rare items, and magic ones too?
            print("'typeLine' and 'name'", items['typeLine'])
            the_keys = list(items.keys())
            print(len(the_keys))
        elif ("Sacrifice at " in items['typeLine']):
            pass
        elif ("Flask" in items['typeLine']):
            #print ('flask', items['typeLine'])
            pass
        else:
            print("else", items['typeLine'], items['name'])
        #pprint.pprint(items)
            #print (items['typeLine'], items['ilvl'], items['name'])

#print(CHARACTERS)
'''
#get active leagues
marketStatUrl = "https://www.pathofexile.com/character-window/get-characters"
resp = s.get(marketStatUrl, cookies = {'POESESSID': values})
leagues = []
for the_character in resp.json():   
    leagues.append((the_character["league"]))
leagues = set(leagues)
print (leagues)


queries = db_queries()'''

#make sure 'owners' are consistant


    
'''for z in CHARACTERS:
    marketStatUrl = ("http://www.pathofexile.com/character-window/get-items?character={n}&accountName=greenmasterflick".format(n=z.name))
    x = s.get(marketStatUrl, cookies = cookie)
    y = x.json()
    print (z.name, y)'''
    

 
