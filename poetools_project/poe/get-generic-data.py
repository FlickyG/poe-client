#!/bin/python3
#import urllib.request, xmltodict
import time, requests, requests_cache
from bs4 import BeautifulSoup
import re
from email._header_value_parser import Section
import psycopg2
import logging, logging.config
import sys #for excepotion handling and printing
import datetime, time #to analyuse how long things take
from xml.dom import minidom

from django.core.management.sql import sql_flush


###
### So we can use our django models here in this script
###
import os
proj_path = "/Users/adam.green/Documents/workspace/poe-client/poetools_project/"
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poetools_project.settings")
sys.path.append(proj_path)
# This is so my local_settings.py gets loaded.
os.chdir(proj_path)
# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from poe.models import ItemCategory, FixCategory, FixType, Fix, Stats, StatNames, FixName, Stats, ItemName


STATS = 0
STAT_NAMES = 0

logging.config.fileConfig('poe_tools_logging.conf')
logger = logging.getLogger(__name__)
start_time = datetime.datetime.now()
logger.info("Staring POE Tools at "+str(start_time))
print(__name__)

def slugify(s):
    """
    Forces a string into lower case, replaces spaces with hyphens
    and removes special characters.
    Accepts: a string
    Returns: a string
    """
    s = s.lower()
    #replaces spaces with hyphens
    s = s.replace(" ", "-")
    #remove all other puncuation
    punc = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~£'
    for x in punc:
        if x in s:
            s = s.replace(x, "")
    # remove numbers
    for x in range(0, 10, 1):
        if str(x) in s:
            s = s.replace(str(x), "")
    return s

def write_item_categories():
    """
    Creates ItemCategory model instances from a pre-defined list and writes
    them to the database
    Accepts: None
    Returns: None
    """
    logger.debug("entering write_item_categories ",)
    list = ['Weapons', 'Clothes', 'Jewelry']
    for x in list:
        try:
            print("write_item_categories", x, slugify(x))
            y = ItemCategory(name = x)
            y.save()
        except:
            logger.debug("psql integrity error when commiting catagory types type (%s)", x)


def write_fix_categories():
    """
    Creates FixCategory model instances from a pre-defined list and saves
    them to the database.
    Accepts: None
    Returns: None
    """        
    logger.debug("entering write_fix_categories ",)
    list = ['Prefix', 'Suffix']
    for x in list:
        try:
            y = FixCategory(name = x)
            y.save()
        except psycopg2.IntegrityError:
            logger.debug("psql integrity error when commiting fix types type (%s)", x)
  
            
def get_item_category(string):
    """
    Queries the database for a ItemCategory object with a given name
    Accepts: string corresponding to the ItemCategory.name
    Returns: The corresponding model object
    """
    logger.debug("entering write_item_categories ",)
    connQ = psycopg2.connect("dbname='poe_data'  user='adam' password='green'")
    currQ = connQ.cursor()
    #print("string", string)
    #print("SELECT * FROM item_categorys WHERE name = {0}".format(string))
    try:
        currQ.execute("SELECT * FROM item_category WHERE name = '{0}'".format(string))
        a = currQ.fetchone()[0] #one()[0]
        return(a)
    except:
        print("entering exception case in get_item_categorys", sys.exc_info()[0])
        #print("exception string in get_item_categorys", string)
    currQ.close()

            
def write_item_type(the_type, list):
    """ 
    Creates ItemType model instances from a list and writes them to the database
    Accepts: A list of ItemType names
    Returns: None
    """    
    logger.debug("entering write_item_type (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='adam' password='green'")
    currQ = connQ.cursor()
    for x in list:
        try:
            #print("name", x)
            currQ.execute("INSERT INTO item_type (name, type_id, slug) "
                        "VALUES (%s, %s, %s)",
             (x, the_type, slugify(x),))           
            connQ.commit()
        except psycopg2.IntegrityError:
            logger.debug("psql integrity error when commiting item types type (%s) (%s)", (the_type, x, ))
            print("psql integrity error when commiting item types type (%s) (%s)", (the_type, x, ))
            connQ.rollback()
            
def get_item_type_id(item):
    """ Queries the database for a ItemType object with a given name
        Accepts: string corresponding to the ItemType.name
        Returns: None
    """
    logger.debug("entering write_item_type_id (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='adam' password='green'")
    currQ = connQ.cursor()
    #for x in list:
    try:
        currQ.mogrify("SELECT id FROM item_type WHERE name = '{0}' ".
            format(item))           
        a = currQ.fetchone()
    except psycopg2.IntegrityError:
        logger.debug("psql integrity error when getting item type ID type (%s)" % item)

    
    
def write_prefix_types(list):
    """ Creates PrefixType model instances from a list and writes them to 
        the database.  Has and intermediate step where it identifies the Prefix 
        model object.
        Accepts: A list of PrefixType names
        Returns: None
    """   
    logger.debug("entering write_prefix_types (%s)", list)
    for x in list:
        try:
            type = FixCategory.objects.get(name = 'Prefix')
            type.fixtype_set.create(name = x)
        except:
            logger.debug("write_prefix_types - Unexpected error:", sys.exc_info()[0], x)
            sys.exit()
            
def write_suffix_types(list):
    """
    Creates SuffixType model instances from a list and writes them to 
    the database.  Has and intermediate step where it identifies the Suffix 
    model object.
    Accepts: A list of SuffixType names
    Returns: None
    """  
    for x in list:
        try:
            type = FixCategory.objects.get(name = 'Suffix')
            type.fixtype_set.create(name = x)
        except:
            print("psql integrity error when commiting suffix types type (%s)", x)
            logger.debug("write_suffix_types - Unexpected error:", sys.exc_info()[0], x)

def make_throttle_hook(timeout=1.0):  # for eve market api calls
    """
    Returns a response hook function which sleeps for `timeout` seconds if
    response is not cached
    """
    def hook(response, **kwargs):
        if not getattr(response, 'from_cache', False):
            time.sleep(timeout)
        return response
    return hook

requests_cache.install_cache('first_go', expires_after = 1)
requests_cache.clear()
s =  requests.Session()
s.hooks = {'response': make_throttle_hook(0.1)}

url_weap = "https://www.pathofexile.com/item-data/weapon"
url_clothes = "http://www.pathofexile.com/item-data/armour"
url_jewelry = "http://www.pathofexile.com/item-data/jewelry"
url_prefixes = "http://www.pathofexile.com/item-data/prefixmod"
url_suffixes = "http://www.pathofexile.com/item-data/suffixmod"




               
def fetch_prefixes(): #layout is different - implicit mods are on the same line
    """ 
    Downloads, parses and calls other methods to save this prefix data from the POE website.
    Accepts: None
    Returns None but prints data
    """
    logger.debug("entering fetch_prefix (%s)", list)
    prefix_types = set()
    stats = set()
    prefixes = []
    try:
        resp = s.get(url_prefixes)
    except:
        print("unable to load URL, quitting")
        sys.exit()
    soup = BeautifulSoup(resp.text, 'html.parser')
    all_items = soup.find_all("div", {"class": "layoutBox1 layoutBoxFull defaultTheme"})
    for item_type in all_items:
        p_type = item_type.find_all("h1", {"class": "topBar last layoutBoxTitle"})[0].text #gets all item catagory names
        prefix_types.add(p_type)
        items = item_type.find_all("table", {"class": "itemDataTable"}) #gets ALL the raw data for each item class
        for each_class in items: # for each prefix class
            data = each_class.find_all("tr") #get the raw data for each line
            y = 1 #first two entries are table formatting aspects
            while y < len(data): # need to collect two 'tr' entries for each item, so use while loop
                prefix = {}
                item_data = []
                prefix["type"] = p_type
                prefix["i_level"] = data[y].find_all("td")[1].get_text()
                name_data = data[y].find_all("td")[0].get_text()
                if "(Master Crafted)" in name_data:
                    prefix["name"] = name_data.split(" (")[0]
                    prefix["master_crafted"] = True
                else:
                    prefix["name"] = data[y].find_all("td")[0].get_text()
                    prefix["master_crafted"] = False
                raw_data = data[y].find_all("td") # grabs all the data from this row of the web page table - each individual stat
                # below strips off the tags and heads 
                mods = [ z for z in re.findall(r">(.*?)<",str(raw_data[2:])) if (z and ((z != ", ") or (z != ", ")))]
                assert len(mods)%2 == 0 #checks there is a evenm number of names to values
                stop = int(len(mods)/2) #used to determine the demark between names and values
                key_results = mods[:stop]
                values_results = mods[stop:]
                assert len(key_results) == len(values_results) #check we have the same number of names and values
                mod_keys = [] 
                mod_values = []
                all_stats = []  # all stats of each prefix
                for x in values_results: #for each stat in this prefeix
                    these_values = []  
                    # the values cover a range
                    if "to" in x:
                        min_value = x.split()[0]
                        max_value = x.split()[2]
                        these_values.append(min_value)
                        these_values.append(max_value)
                        mod_values.append(these_values)
                    else: # if there is a single number and no 'to' 
                        min_value = x
                        max_value = x
                        these_values.append(min_value)
                        these_values.append(max_value)
                        mod_values.append(these_values)
                for x in range(0,stop):
                    test_stat = {}
                    test_stat["implicit_mod_key_"+str(x)] = key_results[x]
                    test_stat["implicit_mod_values_"+str(x)+"_min"] = mod_values[x][0]
                    test_stat["implicit_mod_values_"+str(x)+"_max"] = mod_values[x][1]
                    all_stats.append(test_stat)
                    stats.add((key_results[x], mod_values[x][0], mod_values[x][1])) #use tuples as ordered and hashable
                    #all_the_stats.update(test_stat)
                prefix["stats"] = all_stats
                y = y+1
                prefixes.append(prefix)
    #prefixes = set(prefixes)
    print("length of prefix_types = ", len(prefix_types))
    write_prefix_types(prefix_types)
    stat_names = set()
    for stat in stats:
        stat_names.add(stat[0])
    write_stat_names(stat_names) #unique
    write_stats(stats) #unique
    names = set()
    for x in prefixes:
        names.add((x["type"], x["name"]))
    print("length of prefix names", len(names))
    write_prefix_names(names) # unique
    # make prefixes unique, to stop copying over duplicates from the website
    unique_prefixes = []
    for item in prefixes:
        if item not in unique_prefixes:
            unique_prefixes.append(item)
    write_prefixes(unique_prefixes)
    #for x in unique_prefixes:
    #    print(x)


def write_prefixes(the_list):
    """
    Saves prefix model instances to the database
    Accepts: List of prefix names and values
    Returns: None but prints some data
    """
    logger.debug("entering write_prefixes (%s)", the_list)
    z = 0 #  to count number of database entries
    for x in the_list:
        the_category = FixCategory.objects.get(name = 'Prefix')
        prefix_type = FixType.objects.get(name = x['type'], category = the_category)
        #need to decide if we want a seperate stats table, and make the above sql
        #currQ.execute("SELECT id FROM fix_name WHERE name = (%s) AND type_id = (%s)", (x["name"], prefix_type,))
        name_id = FixName.objects.get(name = x['name'], type = prefix_type)
        for y in x["stats"]:
            for keys, values in y.items():
                if "implicit_mod_key" in keys:
                    stat_name_id = StatNames.objects.get(name = values)#HERE we are overighting the name_id, here it is the description name of the stat, but earlier it was the name of the prefix.  Probably need to add column to the table?
                if "min" in keys:
                    minimum = values
                if "max" in keys:
                    maximum = values
            stat_id = Stats.objects.get(name = stat_name_id, min_value = minimum, max_value = maximum)
            try:
                z = z + 1 #  to count number of database entries
                x2 = Fix(name = name_id, stat = stat_id, i_level = x["i_level"], m_crafted = str(x["master_crafted"]))
            except Exception as e:     
                z = z - 1 #  remove duplicates
                logger.debug(" error when commiting prefixes (%s)", x, e)
    print("length of prefixes written to database ", z)
      
def write_prefix_names(the_set):
    """
    Write the prefixes to the fix_name table
    Accepts: a set of 
    Returns: nothing but prints the number of entries written
    """
    logger.debug("entering write_prefix_names (%s)", the_set)
    z = 0
    for x in the_set:
        try:
            z = z + 1
            try:
                the_category = FixCategory.objects.get(name = 'Prefix')
            except Fix.DoesNotExist as e:
                logger.debug("Fix.DoesNotExist ", e)
            try:
                type_id = FixType.objects.get(name = x[0], category = the_category)
            except FixType.DoesNotExist as e:
                logger.debug("FixType.DoesNotExist ", e)     
            y = FixName(name = x[1], type = type_id)
            y.save()
        except Exception as e:
            z = z - 1
            logger.info("error commiting prefix names (%s)", x)
    print("write_prefix_names z", z) 
    
def write_stat_names(the_set):
    """
    Creates StatName model instances and saves them to the database. Keeps track
    of the number of stats names successfully saved
    Accepts: a set of prefix names
    Returns: None
    """
    global STAT_NAMES
    logger.debug("entering write_stat_names (%s)", list)
    for x in the_set:
        try:
            y = StatNames.objects.get(name = x) #the entry already exists
            pass
        except StatNames.DoesNotExist as e:
            try:
                STAT_NAMES = STAT_NAMES + 1
                y = StatNames(name = x)
                y.save()
            except:
                STAT_NAMES = STAT_NAMES - 1
                logger.debug("write_stat_names - Unexpected error:", sys.exc_info()[0], x)
                sys.exit()
            
         
    
def write_stats(the_set):
    """
    Creates stat model instances and saves them to the database
    Accepts: a set of stats
    Returns: None but keeps track of the number of Stats successfully written to the database 
    """
    global STATS
    logger.debug("entering write_stats (%s)", list)
    for x in the_set:
        try:
            # get id of the stat neame
            the_statname = StatNames.objects.get(name = x[0])
            try:
                y = Stats.objects.get(name = the_statname, min_value = x[1], max_value = x[2])
                pass
            except Stats.DoesNotExist as e:
                y = Stats(name = the_statname, min_value = x[1], max_value = x[2])
                y.save()
                STATS = STATS + 1
        except Exception as e:
            STATS = STATS - 1
            logger.info("write_stats - Unexpected error:")
            sys.exit()

    

def fetch_suffixes(): #layout is different - implicit mods are on the same line
    """
    Downloads the suffix data from the GGG website, extracts the useful info and
    calls other methods in order to save this data to the database
    Accepts: None
    Returns: None but prints useful data along the way
    """
    logger.debug("entering fetch_refix_2 (%s)", list)
    suffix_types = set()
    stats = set()
    suffixes = []
    try:
        resp = s.get(url_suffixes)
    except:
        print("unable to load URL, quitting")
        sys.exit()
    soup = BeautifulSoup(resp.text, 'html.parser')
    all_items = soup.find_all("div", {"class": "layoutBox1 layoutBoxFull defaultTheme"})
    for item_type in all_items:
        p_type = item_type.find_all("h1", {"class": "topBar last layoutBoxTitle"})[0].text #gets all item catagory names
        suffix_types.add(p_type)
        items = item_type.find_all("table", {"class": "itemDataTable"}) #gets ALL the raw data for each item class
        for each_class in items: # for each suffix class
            data = each_class.find_all("tr") #get the raw data for each line
            y = 1 #first two entries are table formatting aspects
            while y < len(data): # need to collect two 'tr' entries for each item, so use while loop
                suffix = {}
                item_data = []
                suffix["type"] = p_type
                suffix["i_level"] = data[y].find_all("td")[1].get_text()
                name_data = data[y].find_all("td")[0].get_text()
                if "(Master Crafted)" in name_data:
                    suffix["name"] = name_data.split(" (")[0]
                    suffix["master_crafted"] = True
                else:
                    suffix["name"] = data[y].find_all("td")[0].get_text()
                    suffix["master_crafted"] = False
                raw_data = data[y].find_all("td") # grabs all the data from this row of the web page table - each individual stat
                # below strips off the tags and heads 
                mods = [ z for z in re.findall(r">(.*?)<",str(raw_data[2:])) if (z and ((z != ", ") or (z != ", ")))]
                assert len(mods)%2 == 0 #checks there is a evenm number of names to values
                stop = int(len(mods)/2) #used to determine the demark between names and values
                key_results = mods[:stop]
                values_results = mods[stop:]
                assert len(key_results) == len(values_results) #check we have the same number of names and values
                mod_keys = [] 
                mod_values = []
                all_stats = []  # all stats of each suffix
                for x in values_results: #for each stat in this prefeix
                    these_values = []  
                    # the values cover a range
                    if "to" in x:
                        min_value = x.split()[0]
                        max_value = x.split()[2]
                        these_values.append(min_value)
                        these_values.append(max_value)
                        mod_values.append(these_values)
                    else: # if there is a single number and no 'to' 
                        min_value = x
                        max_value = x
                        these_values.append(min_value)
                        these_values.append(max_value)
                        mod_values.append(these_values)
                for x in range(0,stop):
                    test_stat = {}
                    test_stat["implicit_mod_key_"+str(x)] = key_results[x]
                    test_stat["implicit_mod_values_"+str(x)+"_min"] = mod_values[x][0]
                    test_stat["implicit_mod_values_"+str(x)+"_max"] = mod_values[x][1]
                    all_stats.append(test_stat)
                    stats.add((key_results[x], mod_values[x][0], mod_values[x][1])) #use tuples as ordered and hashable
                    #all_the_stats.update(test_stat)
                suffix["stats"] = all_stats
                y = y+1
                suffixes.append(suffix)
    write_suffix_types(suffix_types)
    stat_names = set()
    for stat in stats:
        stat_names.add(stat[0])
    ####
    print("length of suffix_types = ", len(suffix_types))
    stat_names = set()
    for stat in stats:
        stat_names.add(stat[0])
    write_stat_names(stat_names) # unique
    write_stats(stats) # unique
    names = set()
    for x in suffixes:
        names.add((x['type'], x["name"]))
    print("length of suffix names", len(names))
    write_suffix_names(names) #unique
    write_suffixes(suffixes)

def write_suffix_names(the_set):
    """
    Creates suffix name model instances and saves them to the databae
    Accepts: a list of suffix names
    Returns: None
    """
    logger.debug("entering write_sufffix_names (%s)", list)
    z = 0
    for x in the_set:
        try:
            z = z + 1
            try:
                the_category = FixCategory.objects.get(name = 'Suffix')
            except Fix.DoesNotExist as e:
                logger.debug("Fix.DoesNotExist ", e)
            try:
                type_id = FixType.objects.get(name = x[0], category = the_category)
            except FixType.DoesNotExist as e:
                logger.debug("FixType.DoesNotExist ", e)     
            y = FixName(name = x[1], type = type_id)
            y.save()
        except Exception as e:
            z = z - 1
            logger.info("error commiting suffix names (%s)", x)
    print("write_suffixnames z", z) 

def write_suffixes(the_list):
    """
    Creates suffix model instances and saves them to the database.  
    Accepts: a list of suffixes
    Returns: None but prints useful info along the way
    """
    logger.debug("entering write_suffixes (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='adam' password='green'")
    currQ = connQ.cursor()
    z = 0 #  to count number of database entries
    for x in the_list:
        the_category = FixCategory.objects.get(name = 'Suffix')
        suffix_type = FixType.objects.get(name = x['type'], category = the_category)
        #need to decide if we want a seperate stats table, and make the above sql
        #currQ.execute("SELECT id FROM fix_name WHERE name = (%s) AND type_id = (%s)", (x["name"], suffix_type,))
        name_id = FixName.objects.get(name = x['name'], type = suffix_type)
        for y in x["stats"]:
            for keys, values in y.items():
                if "implicit_mod_key" in keys:
                    stat_name_id = StatNames.objects.get(name = values)#HERE we are overighting the name_id, here it is the description name of the stat, but earlier it was the name of the suffix.  Probably need to add column to the table?
                if "min" in keys:
                    minimum = values
                if "max" in keys:
                    maximum = values
            stat_id = Stats.objects.get(name = stat_name_id, min_value = minimum, max_value = maximum)
            try:
                z = z + 1 #  to count number of database entries
                x2 = Fix(name = name_id, stat = stat_id, i_level = x["i_level"], m_crafted = str(x["master_crafted"]))
            except Exception as e:     
                z = z - 1 #  remove duplicates
                logger.debug(" error when commiting suffixes (%s)", x, e)
    print("length of suffixes written to database ", z)
     
   
def fetch_weapons():
    """
    Downloads the weapon data from the GGG website, extracts the useful info
    and then calls additional methods in order to save this to the database
    Accepts: None
    Returns: None but prints useful info along the way
    """
    weapon_types = []
    all_stats = set()
    all_weapons = []
    try:
        resp = s.get(url_weap)
    except:
        print("unable to load URL, quitting")
        sys.exit()
    soup = BeautifulSoup(resp.text, 'html.parser')
    weapons = soup.find_all("tr", {"class" : "even"}) 
    weapons[0].find_all("td", {"class": "name"})
    for y in weapons:
        a = y.find_all("td", {"class": "name"}) 
    all_items = soup.find_all("div", {"class": "layoutBox1 layoutBoxFull defaultTheme"})    
    for item_type in all_items:
        w_type = item_type.find_all("h1", {"class": "topBar last layoutBoxTitle"})[0].text #gets all item catagory names
        weapon_types.append(w_type)
    #write_weapon_types(weapon_types)
    # write weapon types to item_type table, look up the item_category
    type = get_item_category("Weapons")
    write_item_type(type, weapon_types)
    # connect to database
    connQ = psycopg2.connect("dbname='poe_data'  user='adam' password='green'")
    currQ = connQ.cursor()
    currQ.execute("SELECT item_type.id, item_type.name FROM item_type "
                    "JOIN item_category on item_category.id = item_type.type_id "
                    "WHERE item_category.name = 'Weapons'")
    w_id = currQ.fetchall()
    weapon_types = dict((y, x) for x, y in w_id) # dictionary of ids and strings
    for item_type in all_items:
        items = item_type.find_all("table", {"class": "itemDataTable"}) #gets ALL the raw data for each item class
        # extract from the dictonary the id for the weapon
        w_type = weapon_types[item_type.find_all("h1", {"class": "topBar last layoutBoxTitle"})[0].text] #gets all item catagory names
        for item_data in items: # for each weaspon class
            data = item_data.find_all("tr") #get the raw data
            x = 2 #first two entries are table formatting aspects
            while x < len(data): # need to collect two 'tr' entries for each item, so use while loop
                item_data = []
                item = {}
                raw_data = data[x].find_all("td")
                item["large_url"] = raw_data[0].find_all("img")[0]["data-large-image"]
                item["small_url"] = raw_data[0].find_all("img")[0]["src"]
                item["name"] = raw_data[1].get_text()
                item["i_level"] = raw_data[2].get_text()
                item["min_dmg"] = raw_data[3].get_text().split()[0]
                item["max_dmg"] = raw_data[3].get_text().split()[2]
                item["aps"] = raw_data[4].get_text()
                item["dps"] = raw_data[5].get_text()
                item["req_str"] = raw_data[6].get_text()
                item["req_dex"] = raw_data[7].get_text()
                item["req_int"] = raw_data[8].get_text()
                item["slug"] = slugify(raw_data[1].get_text())
                #need the index from the item type table
                item["type_id"] = w_type change this to model
                x = x+1                
                mods = [ z for z in re.findall(r">(.*?)<",str(data[x])) if (z and ((z != ", ") or (z != ", ")))]
                #input("Press Enter to continue...")
                if len(mods) > 0:
                    assert len(mods)%2 == 0 #checks there is a evenm number of names to values
                    stop = int(len(mods)/2) #used to determine the demark between names and values
                    key_results = mods[:stop]
                    values_results = mods[stop:]
                    assert len(key_results) == len(values_results) #check we have the same number of names and values
                    mod_keys = [] 
                    mod_values = []
                    stats = []  # all stats of each suffix
                    for z in values_results: #for each stat in this prefeix
                        these_values = []  
                        # the values cover a range
                        if "to" in z:
                            min_value = z.split()[0]
                            max_value = z.split()[2]
                            these_values.append(min_value)
                            these_values.append(max_value)
                            mod_values.append(these_values)
                        else: # if there is a single number and no 'to' 
                            min_value = z
                            max_value = z
                            these_values.append(min_value)
                            these_values.append(max_value)
                            mod_values.append(these_values)
                    for a in range(0,stop):
                        test_stat = {}
                        test_stat["implicit_mod_key_"+str(a)] = key_results[a]
                        test_stat["implicit_mod_values_"+str(a)+"_min"] = mod_values[a][0]
                        test_stat["implicit_mod_values_"+str(a)+"_max"] = mod_values[a][1]
                        stats.append(test_stat)
                        all_stats.add((key_results[a], mod_values[a][0], mod_values[a][1])) #use tuples as ordered and hashable
                    item["implicits"] = stats     
                all_weapons.append(item)
                x = x+1
    stat_names = set()
    for stat in all_stats:
        stat_names.add(stat[0])
    write_stat_names(stat_names)
    write_stats(all_stats)
    write_weapon_names(all_weapons)
    print("length of weapon_names", len(all_weapons))
    print("length of weapon_stats", write_weapon_stats(all_weapons))
    
def write_weapon_names(list):
    logger.debug("entering write_weapon_names (%s)", list)
    z = 0  
    for x in list:
        try:
            y = ItemName(
                    name = x["name"],
                    i_level = x["i_level"], 
                    min_dmg = x["max_dmg"],
                    max_dmg = x["max_dmg"],
                    aps = x['aps'],
                    dps = x['dps'],
                    req_str = x['req_str'],
                    req_dex = x['req_dex'],
                    req_int = x['req_int'],
                    large_url = x["large_url"],
                    small_url = x["small_url"],
                    type = x["type_id"]
                )
            z.save()
            z = z + 1
            """
            currQ.execute("INSERT INTO item_name (name, i_level, min_dmg, max_dmg,"
                          "aps, dps, req_str, req_dex, req_int, large_url, small_url, type_id, slug)"
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                          (x["name"], x["i_level"], x["min_dmg"], x["max_dmg"],
                           x["aps"], x["dps"], x["req_str"], x["req_dex"], x["req_int"], x["large_url"],
                           x["small_url"], x["type_id"], x["slug"]))
            """           
        except Exception as e:
            z = z - 1
            print("error when commiting weapon names (%s)", e)
            logger.debug("error when commiting weapon names (%s)", e)
    print("number of weapon names writtent to database", z) 

def write_weapon_stats(list):
    logger.debug("entering write_weapon_stats (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='adam' password='green'")
    currQ = connQ.cursor()
    z = 0
    for x in list:
        query = currQ.execute("""SELECT id FROM item_name WHERE name = %s""", (x["name"],))
        #print("query")
        #currQ.execute(query)
        w_id = currQ.fetchone()
        if "implicits" in x:
            for y in x["implicits"]:
                for keys, values in y.items():
                    if "implicit_mod_key" in keys:
                        currQ.execute("SELECT id FROM stat_names WHERE name = (%s)",
                                  (values,))
                        stat_id = currQ.fetchone()[0]
                for keys, values in y.items():   
                    if "min" in keys:
                        currQ.execute("SELECT min_value FROM stats WHERE name_id = (%s)",
                                  (stat_id,))
                        min = currQ.fetchone()[0]
                        min = values
                for keys, values in y.items():   
                    if "max" in keys:
                        currQ.execute("SELECT max_value FROM stats WHERE name_id = (%s)",
                                  (stat_id,))
                        max = currQ.fetchone()[0]
                        max = values
                currQ.execute("SELECT id FROM stats WHERE name_id = (%s) AND min_value = (%s) AND max_value = (%s)",
                              (stat_id, min, max,))
                s_id = currQ.fetchone()
                try:
                    z = z + 1
                    currQ.execute("INSERT INTO item_stat (i_id, s_id) VALUES (%s, %s)",
                        (w_id, s_id,))           
                    connQ.commit()
                except psycopg2.IntegrityError:
                    z = z - 1
                    logger.debug("psql integrity error when commiting weapon stats (%s)", x)
    return(z)
   
def fetch_clothes():
    clothes_types = []
    all_stats = set()
    all_clothes = []
    try:
        resp = s.get(url_clothes)
    except:
        print("unable to load URL, quitting")
        sys.exit()
    soup = BeautifulSoup(resp.text, 'html.parser')
    #print all clothes names
    clothes = soup.find_all("tr", {"class" : "even"}) 
    clothes[0].find_all("td", {"class": "name"})
    for y in clothes:
        a = y.find_all("td", {"class": "name"}) 
    all_items = soup.find_all("div", {"class": "layoutBox1 layoutBoxFull defaultTheme"})    
    for item_type in all_items:
        c_type = item_type.find_all("h1", {"class": "topBar last layoutBoxTitle"})[0].text #gets all item catagory names
        clothes_types.append(c_type)
    #write clothes types
    type = get_item_category("Clothes")
    write_item_type(type, clothes_types)   
    # connect to database
    connQ = psycopg2.connect("dbname='poe_data'  user='adam' password='green'")
    currQ = connQ.cursor()
    currQ.execute("SELECT item_type.id, item_type.name FROM item_type "
                    "JOIN item_category on item_category.id = item_type.type_id "
                    "WHERE item_category.name = 'Clothes'")
    c_id = currQ.fetchall()
    clothing_types = dict((y, x) for x, y in c_id)
    for item_type in all_items:
        #write_clothes_types(clothes_types)
        items = item_type.find_all("table", {"class": "itemDataTable"}) #gets ALL the raw data for each item class
        c_type = clothing_types[item_type.find_all("h1", {"class": "topBar last layoutBoxTitle"})[0].text] #gets all item catagory names
        for item_data in items: # for each weaspon class
            data = item_data.find_all("tr") #get the raw data
            x = 2 #first two entries are table formatting aspects
            while x < len(data): # need to collect two 'tr' entries for each item, so use while loop
                #input("Press Enter to continue...")
                item_data = []
                item = {}
                raw_data = data[x].find_all("td")
                #item["c_type"] = c_type
                item["large_url"] = raw_data[0].find_all("img")[0]["data-large-image"]
                item["small_url"] = raw_data[0].find_all("img")[0]["src"]
                item["name"] = raw_data[1].get_text()
                item["i_level"] = raw_data[2].get_text()
                #item["damage"] = raw_data[3].get_text()
                item["armour"] = raw_data[3].get_text()
                item["evasion"] = raw_data[4].get_text()
                item["energy_shield"] = raw_data[5].get_text()
                item["req_str"] = raw_data[6].get_text()
                item["req_dex"] = raw_data[7].get_text()
                item["req_int"] = raw_data[8].get_text()
                item["type_id"] = c_type
                item["slug"] = raw_data[1].get_text()
                #urls = raw_data[0].find_all("img")
                x = x+1                
                #implicits = data[x].find_all("td")
                mods = [ z for z in re.findall(r">(.*?)<",str(data[x])) if (z and ((z != ", ") or (z != ", ")))]
                #input("Press Enter to continue...")
                if len(mods) > 0:
                    if "Dummy Stat Display Nothing" in mods:
                        mods.remove("Dummy Stat Display Nothing")
                    assert len(mods)%2 == 0 #checks there is a evenm number of names to values
                    stop = int(len(mods)/2) #used to determine the demark between names and values
                    key_results = mods[:stop]
                    values_results = mods[stop:]
                    assert len(key_results) == len(values_results) #check we have the same number of names and values
                    mod_keys = [] 
                    mod_values = []
                    stats = []  # all stats of each suffix
                    for z in values_results: #for each stat in this prefeix
                        these_values = []  
                        # the values cover a range
                        if "to" in z:
                            min_value = z.split()[0]
                            max_value = z.split()[2]
                            these_values.append(min_value)
                            these_values.append(max_value)
                            mod_values.append(these_values)
                        else: # if there is a single number and no 'to' 
                            min_value = z
                            max_value = z
                            these_values.append(min_value)
                            these_values.append(max_value)
                            mod_values.append(these_values)
                    for a in range(0,stop):
                        test_stat = {}
                        test_stat["implicit_mod_key_"+str(a)] = key_results[a]
                        test_stat["implicit_mod_values_"+str(a)+"_min"] = mod_values[a][0]
                        test_stat["implicit_mod_values_"+str(a)+"_max"] = mod_values[a][1]
                        stats.append(test_stat)
                        all_stats.add((key_results[a], mod_values[a][0], mod_values[a][1])) #use tuples as ordered and hashable
                    item["implicits"] = stats     
                all_clothes.append(item)
                x = x+1
    stat_names = set()
    for stat in all_stats:
        stat_names.add(stat[0])
    write_stat_names(stat_names)
    write_stats(all_stats)
    #write_clothes_types(clothes_types)
    write_clothes_names(all_clothes)
    #write_clothes_stats(all_clothes)
    print("length of clothes_names", len(all_clothes))
    print("length of clothes_stats", write_clothes_stats(all_clothes))
    
def write_clothes_names(list):
    logger.debug("entering write_clothes_names (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='adam' password='green'")
    currQ = connQ.cursor()  
    for x in list:
        try:
            pass
            currQ.execute("INSERT INTO item_name (name, i_level, armour, evasion,"
                          "energy_shield, req_str, req_dex, req_int, large_url, small_url, type_id, slug)"
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                          (x["name"], x["i_level"], x["armour"], x["evasion"],
                           x["energy_shield"], x["req_str"], x["req_dex"], x["req_int"], x["large_url"],
                           x["small_url"],x["type_id"], x["slug"]))           
            connQ.commit()
        except psycopg2.IntegrityError:
            logger.debug("psql integrity error when commiting clothes names (%s)", x)
            connQ.rollback() 

def write_clothes_stats(list):
    logger.debug("entering write_clothes_stats (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='adam' password='green'")
    currQ = connQ.cursor()  
    z = 0
    for x in list:
        currQ.execute("SELECT id FROM item_name WHERE name = %s", (x["name"],))
        w_id = currQ.fetchone()
        if "implicits" in x:
            for y in x["implicits"]:
                for keys, values in y.items():
                    if "implicit_mod_key" in keys:
                        currQ.execute("SELECT id FROM stat_names WHERE name = (%s)",
                                  (values,))
                        stat_id = currQ.fetchone()[0]
                for keys, values in y.items():   
                    if "min" in keys:
                        currQ.execute("SELECT min_value FROM stats WHERE name_id = (%s)",
                                  (stat_id,))
                        min = currQ.fetchone()[0]
                        min = values
                for keys, values in y.items():   
                    if "max" in keys:
                        currQ.execute("SELECT max_value FROM stats WHERE name_id = (%s)",
                                  (stat_id,))
                        max = currQ.fetchone()[0]
                        max = values
                currQ.execute("SELECT id FROM stats WHERE name_id = (%s) AND min_value = (%s) AND max_value = (%s)",
                              (stat_id, min, max,))
                s_id = currQ.fetchone()
                try:
                    z = z + 1
                    currQ.execute("INSERT INTO item_stat (i_id, s_id) VALUES (%s, %s)",
                        (w_id, s_id,))           
                    connQ.commit()
                except psycopg2.IntegrityError:
                    z = z -1
                    logger.debug("psql integrity error when commiting clothes stats (%s)", x)
    return(z)

def fetch_jewelry():
    jewelry_types = []
    all_stats = set()
    all_jewelry = []
    try:
        resp = s.get(url_jewelry)
    except:
        print("unable to load URL, quitting")
        sys.exit()
    soup = BeautifulSoup(resp.text, 'html.parser')
    #print all jewelry names
    jewelry = soup.find_all("tr", {"class" : "even"}) 
    jewelry[0].find_all("td", {"class": "name"})
    for y in jewelry:
        a = y.find_all("td", {"class": "name"}) 
    all_items = soup.find_all("div", {"class": "layoutBox1 layoutBoxFull defaultTheme"})    
    for item_type in all_items:
        j_type = item_type.find_all("h1", {"class": "topBar last layoutBoxTitle"})[0].text #gets all item catagory names
        jewelry_types.append(j_type)
    #write_jewelry_types(jewelry_types)
    # write item types
    type = get_item_category("Jewelry")
    write_item_type(type, jewelry_types)
    connQ = psycopg2.connect("dbname='poe_data'  user='adam' password='green'")
    currQ = connQ.cursor()
    currQ.execute("SELECT item_type.id, item_type.name FROM item_type "
                    "JOIN item_category on item_category.id = item_type.type_id "
                    "WHERE item_category.name = 'Jewelry'")
    j_id = currQ.fetchall()
    jewelry_types = dict((y, x) for x, y in j_id)
    for item_type in all_items:
        j_type = jewelry_types[item_type.find_all("h1", {"class": "topBar last layoutBoxTitle"})[0].text] #gets all item catagory names
        #write_jewelry_types(jewelry_types)
        items = item_type.find_all("table", {"class": "itemDataTable"}) #gets ALL the raw data for each item class
        for item_data in items: # for each weaspon class
            data = item_data.find_all("tr") #get the raw data
            x = 2 #first two entries are table formatting aspects
            while x < len(data): # need to collect two 'tr' entries for each item, so use while loop
                #print(data[x])
                #input("Press Enter to continue...")
                #item_data = []
                item = {}
                raw_data = data[x].find_all("td")
                #item["j_type"] = j_type
                item["large_url"] = raw_data[0].find_all("img")[0]["data-large-image"]
                item["small_url"] = raw_data[0].find_all("img")[0]["src"]
                item["name"] = raw_data[1].get_text()
                item["i_level"] = raw_data[2].get_text()     
                item["type_id"] = j_type 
                item["slug"] = raw_data[1].get_text()
                key_results = [ x for x in re.findall(r">(.*?)<",str(raw_data[3])) if x]
                value_results = [ x for x in re.findall(r">(.*?)<",str(raw_data[4])) if x]
                stats = []
                mod_keys = key_results
                mod_values = []
                # find implicit values
                if item["name"] == "Undying Flesh Talisman":
                        mod_values = [['0','0'],['1', '1'],['1','1'],['0','0']]   
                else:
                    for y in value_results:
                        these_values = []  
                        # the values cover a range
                        if "to" in y:
                            min_value = y.split()[0]
                            max_value = y.split()[2]
                            these_values.append(min_value)
                            these_values.append(max_value)
                            mod_values.append(these_values)
                        else: # if there is a single number and no 'to' 
                            min_value = y
                            max_value = y
                            these_values.append(min_value)
                            these_values.append(max_value)
                            mod_values.append(these_values)
                assert len(mod_keys) == len(mod_values) # sense check we're passing these correctly
                number_of_mods = len(mod_keys)
                for a in range(0,number_of_mods):
                    test_stat = {}
                    test_stat["implicit_mod_key_"+str(a)] = mod_keys[a]
                    test_stat["implicit_mod_values_"+str(a)+"_min"] = mod_values[a][0]
                    test_stat["implicit_mod_values_"+str(a)+"_max"] = mod_values[a][1]
                    stats.append(test_stat)
                    all_stats.add((key_results[a], mod_values[a][0], mod_values[a][1])) #use tuples as ordered and hashable
                item["implicits"] = stats
                x = x+1
                all_jewelry.append(item)
    stat_names = set()
    for stat in all_stats:
        stat_names.add(stat[0])
    write_stat_names(stat_names)
    write_stats(all_stats)
    #write_jewelry_types(jewelry_types)
    write_jewelry_names(all_jewelry)
    jew_names = set()
    for x in all_jewelry:
        jew_names.add(x["name"]) 
    print("jewerly names written to database", len(jew_names))
    #write_jewelry_stats(all_jewelry)
    print("jewelry stats written to data base", write_jewelry_stats(all_jewelry))
    
def write_jewelry_names(list):
    logger.debug("entering write_jewelry_names (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='adam' password='green'")
    currQ = connQ.cursor()  
    for x in list:
        try:
            pass
            currQ.execute("INSERT INTO item_name (name, i_level, large_url, "
                                "small_url, type_id, slug)"
                          "VALUES (%s, %s, %s, %s, %s, %s)",
                          (x["name"], x["i_level"], x["large_url"],
                                x["small_url"],x["type_id"], x["slug"]))           
            connQ.commit()
        except psycopg2.IntegrityError:
            logger.debug("psql integrity error when commiting jewelry names (%s)", x)
            connQ.rollback() 

def write_jewelry_stats(list):
    logger.debug("entering write_jewelry_stats (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='adam' password='green'")
    currQ = connQ.cursor()
    z = 0 
    for x in list:
        currQ.execute("SELECT id FROM item_name WHERE name = %s", (x["name"],))
        w_id = currQ.fetchone()
        if "implicits" in x:
            for y in x["implicits"]:
                for keys, values in y.items():
                    if "implicit_mod_key" in keys:
                        currQ.execute("SELECT id FROM stat_names WHERE name = (%s)",
                                  (values,))
                        stat_id = currQ.fetchone()[0]
                for keys, values in y.items():   
                    if "min" in keys:
                        currQ.execute("SELECT min_value FROM stats WHERE name_id = (%s)",
                                  (stat_id,))
                        min = currQ.fetchone()[0]
                        min = values
                for keys, values in y.items():   
                    if "max" in keys:
                        currQ.execute("SELECT max_value FROM stats WHERE name_id = (%s)",
                                  (stat_id,))
                        max = currQ.fetchone()[0]
                        max = values
                currQ.execute("SELECT id FROM stats WHERE name_id = (%s) AND min_value = (%s) AND max_value = (%s)",
                              (stat_id, min, max,))
                s_id = currQ.fetchone()[0]
                try:
                    z = z + 1
                    currQ.execute("INSERT INTO item_stat (i_id, s_id) VALUES (%s, %s)",
                        (w_id, s_id,))           
                    connQ.commit()
                except psycopg2.IntegrityError:
                    z = z - 1
                    logger.debug("psql integrity error when commiting jewelry stats (%s)", x)
    return(z)

    

write_item_categories()
write_fix_categories()

fetch_prefixes()
fetch_suffixes()
fetch_weapons()
fetch_clothes()
fetch_jewelry()

"""
my_fixname = FixName.objects.get(id = 11)
my_stat = Stats.objects.get(id = 1)
my_fix  = Fix(name = my_fixname, stat = my_stat, i_level = 1, m_crafted = True)

my_fixcategory = FixCategory(name = "adam")
my_fixcategory.save()

my_fixType = FixType(category = my_fixcategory, name = "green")
my_fixType.save()

my_statnames = StatNames(name = "andy")
my_statnames.save()

the_stat = Stats(min_value = 1, max_value = 111, name = my_statnames)
the_stat.save()

the_name = FixName(type = my_fixType, name = "watson")
the_name.save()

the_fix = Fix(name = the_name, stat = the_stat, i_level = 1, m_crafted = False)
the_fix.save()
"""
print("number of stats written to database", STATS)
print("number of stat_names written to database", STAT_NAMES)

logger.info("Exiting POE Tools, it took "+str(datetime.datetime.now() - start_time))


