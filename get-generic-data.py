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


logging.config.fileConfig('poe_tools_logging.conf')
logger = logging.getLogger(__name__)
start_time = datetime.datetime.now()
logger.info("Staring POE Tools at "+str(start_time))
print(__name__)

def write_weapon_types(list):
    logger.debug("entering write_weapon_types (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='poetools' password='monkey'")
    currQ = connQ.cursor()
    for x in list:
        try:
            currQ.execute("INSERT INTO weapon_types (type) "
                        "VALUES (%s)",
             [x])           
            connQ.commit()
        except psycopg2.IntegrityError:
            logger.debug("psql integrity error when commiting weapons types type (%s)", x)
            connQ.rollback()

def write_clothing_types(list):
    logger.debug("entering write_clothing_types (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='poetools' password='monkey'")
    currQ = connQ.cursor()
    for x in list:
        try:
            currQ.execute("INSERT INTO clothing_types (type) "
                        "VALUES (%s)",
             [x])           
            connQ.commit()
        except psycopg2.IntegrityError:
            logger.debug("psql integrity error when commiting clothing types type (%s)", x)
            connQ.rollback()  
    
def write_jewelry_types(list):
    logger.debug("entering write_jewelry_types (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='poetools' password='monkey'")
    currQ = connQ.cursor()
    for x in list:
        try:
            currQ.execute("INSERT INTO jewelry_types (type) "
                        "VALUES (%s)",
             [x])           
            connQ.commit()
        except psycopg2.IntegrityError:
            logger.debug("psql integrity error when commiting jewelry types type (%s)", x)
            connQ.rollback()
    
def write_prefix_types(list):
    logger.debug("entering write_prefix_types (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='poetools' password='monkey'")
    currQ = connQ.cursor()
    for x in list:
        try:
            currQ.execute("INSERT INTO prefix_types (type) "
                        "VALUES (%s)",
             [x])           
            connQ.commit()
        except psycopg2.IntegrityError:
            logger.debug("psql integrity error when commiting prefix types type (%s)", x)
            connQ.rollback()
            
def write_suffix_types(list):
    logger.debug("entering write_suffix_types (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='poetools' password='monkey'")
    currQ = connQ.cursor()
    for x in list:
        try:
            currQ.execute("INSERT INTO suffix_types (type) "
                        "VALUES (%s)",
             [x])           
            connQ.commit()
        except psycopg2.IntegrityError:
            logger.debug("psql integrity error when commiting suffix types type (%s)", x)
            connQ.rollback()  

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

url_weap = "https://www.pathofexile.com/item-data/weapon"
url_clothes = "http://www.pathofexile.com/item-data/armour"
url_jewelry = "http://www.pathofexile.com/item-data/jewelry"
url_prefixes = "http://www.pathofexile.com/item-data/prefixmod"
url_suffixes = "http://www.pathofexile.com/item-data/suffixmod"


        
def parse_clothing(item_data):
    item = {}
    item["large_url"] = item_data[0][0].find_all("img")[0]["data-large-image"]
    item["small_url"] = item_data[0][0].find_all("img")[0]["src"]
    item["name"] = item_data[0][1].get_text()
    item["item_level"] = item_data[0][2].get_text()
    item["armour"] = item_data[0][3].get_text()
    item["evasion_rating"] = item_data[0][4].get_text()
    item["energy_shield"] = item_data[0][5].get_text()
    item["req_str"] = item_data[0][6].get_text()
    item["req_dex"] = item_data[0][7].get_text()
    item["req_int"] = item_data[0][8].get_text()
    # generate a list of dictionaries for the mods
    try:
        # find implcit type, which is the keys
        item_data[1][0].get_text()
        implicit_mods = {}
        test_text = str(item_data[1][0])
        key_results = [ x for x in re.findall(r">(.*?)<",test_text) if x]
        mod_keys = []
        mod_values = []
        for x in key_results:
            if 'Dummy Stat Display Nothing' in x:
                pass # skip these
            else:
                mod_keys.append(x)
        # find implicit values
        test_text = str(item_data[1][1])
        value_results = [x for x in re.findall(r">(.*?)<",test_text) if x]
        for x in value_results:
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
        # check lists are the same length
        assert len(mod_keys) == len(mod_values) # sense check we're passing these correctly
        number_of_mods = len(mod_keys)
        for x in range(0,number_of_mods):
            item["implicit_mod_key_"+str(x)] = mod_keys[x]
            item["implicit_mod_values_"+str(x)+"_min"] = mod_values[x][0]
            item["implicit_mod_values_"+str(x)+"_max"] = mod_values[x][1]
    except IndexError: # not all items have implicit mods
        pass
    
def parse_jewelry(item_data):
    item = {}
    item["large_url"] = item_data[0][0].find_all("img")[0]["data-large-image"]
    item["small_url"] = item_data[0][0].find_all("img")[0]["src"]
    item["name"] = item_data[0][1].get_text()
    item["item_level"] = item_data[0][2].get_text()
    #<td>Zombie Quantity<br/>Base Number Of Skeletons Allowed<br/>Spectre Quantity<br/>Local Stat Monsters Pick Up Item<br/></td>
    key_results = [ x for x in re.findall(r">(.*?)<",str(item_data[0][3])) if x]
    value_results = [ x for x in re.findall(r">(.*?)<",str(item_data[0][4])) if x]
    mod_keys = []
    mod_values = []
    for x in key_results:
        if 'Dummy Stat Display Nothing' in x:
            pass # skip these
        else:
            mod_keys.append(x)
    # find implicit values
    if item["name"] == "Undying Flesh Talisman":
            mod_values = [['0','0'],['1', '1'],['1','1'],['0','0']]   
    else:
        for x in value_results:
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
    assert len(mod_keys) == len(mod_values) # sense check we're passing these correctly
    number_of_mods = len(mod_keys)
    for x in range(0,number_of_mods):
        item["implicit_mod_key_"+str(x)] = mod_keys[x]
        item["implicit_mod_values_"+str(x)+"_min"] = mod_values[x][0]
        item["implicit_mod_values_"+str(x)+"_max"] = mod_values[x][1]
    
def fetch_clothes():
    clothing_types = []
    resp = s.get(url_clothes)
    soup = BeautifulSoup(resp.text, 'html.parser')
    clothes = soup.find_all("tr") 
    clothes[0].find_all("td", {"class": "name"})
    for y in clothes:
        a = y.find_all("td", {"class": "name"})
        if len(a) > 0:
            pass
            #print (a[0].text)        
    all_items = soup.find_all("div", {"class": "layoutBox1 layoutBoxFull defaultTheme"})
    for item_type in all_items:
        c_type = item_type.find_all("h1", {"class": "topBar last layoutBoxTitle"})[0].text #gets all item catagory names
        #print("c_type", c_type)
        clothing_types.append(c_type)
        items = item_type.find_all("table", {"class": "itemDataTable"}) #gets ALL the raw data for each item class
        for item_data in items: # for each clothing class
            data = item_data.find_all("tr") #get the raw data
            x = 2 #first two entries are table formatting aspects
            while x < len(data): # need to collect two 'tr' entries for each item, so use while loop
                item_data = []
                raw_data = data[x].find_all("td")
                item_data.append(raw_data)
                x = x+1
                implicits = data[x].find_all("td")
                item_data.append(implicits)
                item = parse_clothing(item_data)
                x = x+1
                #input("Press Enter to continue...")
    write_clothing_types(clothing_types)

def fetch_jewelry(): #layout is different - implicit mods are on the same line
    jewelry_types = []
    resp = s.get(url_jewelry)
    soup = BeautifulSoup(resp.text, 'html.parser')
    jewelry = soup.find_all("tr") 
    jewelry[0].find_all("td", {"class": "name"})
    for y in jewelry:
        a = y.find_all("td", {"class": "name"})
        if len(a) > 0:
            pass
            #print (a[0].text)   
    all_items = soup.find_all("div", {"class": "layoutBox1 layoutBoxFull defaultTheme"})
    for item_type in all_items:
        j_type = item_type.find_all("h1", {"class": "topBar last layoutBoxTitle"})[0].text #gets all item catagory names
        jewelry_types.append(j_type)
        items = item_type.find_all("table", {"class": "itemDataTable"}) #gets ALL the raw data for each item class
        for item_data in items: # for each clothing class
            data = item_data.find_all("tr") #get the raw data
            x = 2 #first two entries are table formatting aspects
            while x < len(data): # need to collect two 'tr' entries for each item, so use while loop
                item_data = []
                raw_data = data[x].find_all("td")
                item_data.append(raw_data)
                parse_jewelry(item_data)
                x = x+1
    write_jewelry_types(jewelry_types)

def get_prefix_types(key):
    prefix_types = {}
    logger.debug("entering write_clothing_types (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='poetools' password='monkey'")
    currQ = connQ.cursor()
    try:
        currQ.execute("SELECT * FROM prefix_types")
        a = currQ.fetchall()
        print("he")
        temp_prefixes = []
        for x in a:
            temp_prefixes.append(x[::-1])
        prefix_types = dict(temp_prefixes)
        return(prefix_types[key])
    except:
        print("entering exception case in get_prefix_types", sys.exc_info()[0])
    currQ.close()
               
def fetch_prefixes(): #layout is different - implicit mods are on the same line
    logger.debug("entering fetch_refix_2 (%s)", list)
    prefix_types = set()
    stats = set()
    prefixes = []
    resp = s.get(url_prefixes)
    soup = BeautifulSoup(resp.text, 'html.parser')
    all_items = soup.find_all("div", {"class": "layoutBox1 layoutBoxFull defaultTheme"})
    for item_type in all_items:
        p_type = item_type.find_all("h1", {"class": "topBar last layoutBoxTitle"})[0].text #gets all item catagory names
        prefix_types.add(p_type)
        #print("prefix type", p_type)
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
    write_prefix_types(prefix_types)
    stat_names = set()
    for stat in stats:
        stat_names.add(stat[0])
    write_stat_names(stat_names)
    write_stats(stats)
    write_prefix_names(prefixes)
    write_prefixes(prefixes)

def write_prefixes(the_list):
    logger.debug("entering write_prefixes (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='poetools' password='monkey'")
    currQ = connQ.cursor()   
    for x in the_list:
        print("x in list", x, x["name"])
        currQ.execute("SELECT id FROM prefix_types WHERE type = (%s)", (x["type"],))
        prefix_type = currQ.fetchone()[0]
        currQ.execute("SELECT id FROM prefix_names WHERE name = (%s)", (x["name"],))
        name_id = currQ.fetchone()[0]
        print("£ name_id x[name]", name_id, x["name"])
        for y in x["stats"]:
            #print(y)
            for keys, values in y.items():
                #print(keys, values)
                if "implicit_mod_key" in keys:
                    #print(values)
                    currQ.execute("SELECT id FROM stat_names WHERE name = (%s)", (values,))
                    name_id = currQ.fetchone()[0]  HERE we are overighting the name_id, here it is the description name of the stat, but earlier it was the name of the prefix.  Probably need to add column to the table?
                if "min" in keys:
                    minimum = values
                if "max" in keys:
                    maximum = values
            currQ.execute("SELECT id FROM stats WHERE name_id = (%s) AND min_value = (%s) AND max_value = (%s)",
                          (name_id, minimum, maximum))
            stat_id = currQ.fetchone()[0]
            #print("data (%s)", (prefix_type, name_id, x["master_crafted"], stat_id))
            try:
                currQ.execute("INSERT INTO prefixes (type_id, name_id, i_level, crafted, stat) "
                              "VALUES (%s, %s, %s, %s, %s)",
                              (prefix_type, name_id, x["i_level"], str(x["master_crafted"]), stat_id,))           
                connQ.commit()
            except psycopg2.IntegrityError:
                logger.debug("psql integrity error when commiting prefixes (%s)", x)
                connQ.rollback() 
        #print("prefix_type, x[type], name_id, x[name]", prefix_type, x["type"], name_id, x["name"])

      
def write_prefix_names(the_set):
    logger.debug("entering write_prefix_names (%s)", the_set)
    names = set()
    for x in the_set:
        names.add(x["name"])
    connQ = psycopg2.connect("dbname='poe_data'  user='poetools' password='monkey'")
    currQ = connQ.cursor()
    for x in names:
        try:
            currQ.execute("INSERT INTO prefix_names (name) "
                        "VALUES (%s)",
                       (x,))           
            connQ.commit()
        except psycopg2.IntegrityError:
            logger.info("psql integrity error when commiting prefix names (%s)", x)
            connQ.rollback() 
    
def write_stat_names(the_set):
    logger.debug("entering write_stat_names (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='poetools' password='monkey'")
    currQ = connQ.cursor()
    for x in the_set:
        try:
            currQ.execute("INSERT INTO stat_names (name) "
                        "VALUES (%s)",
                       (x,))           
            connQ.commit()
        except psycopg2.IntegrityError:
            logger.debug("psql integrity error when commiting stat names (%s)", x)
            connQ.rollback()     
    
def write_stats(the_set):
    logger.debug("entering write_stats (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='poetools' password='monkey'")
    currQ = connQ.cursor()
    for x in the_set:
        try:
            # get id of the stat neame
            currQ.execute("SELECT id FROM stat_names WHERE name = %s", 
                          (x[0],))
            stat_name = currQ.fetchone()
            currQ.execute("INSERT INTO stats (name_id, min_value, max_value) "
                        "VALUES (%s, %s, %s)",
                        (stat_name, x[1], x[2]))           
            connQ.commit()
        except psycopg2.IntegrityError:
            logger.debug("psql integrity error when commiting stats  (%s)", x)
            connQ.rollback()  
    

def fetch_suffixes(): #layout is different - implicit mods are on the same line
    print("hello world")
    logger.debug("entering fetch_refix_2 (%s)", list)
    suffix_types = set()
    stats = set()
    suffixes = []
    resp = s.get(url_suffixes)
    soup = BeautifulSoup(resp.text, 'html.parser')
    all_items = soup.find_all("div", {"class": "layoutBox1 layoutBoxFull defaultTheme"})
    for item_type in all_items:
        p_type = item_type.find_all("h1", {"class": "topBar last layoutBoxTitle"})[0].text #gets all item catagory names
        suffix_types.add(p_type)
        #print("suffix type", p_type)
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
    write_stat_names(stat_names)
    write_stats(stats)
    write_suffix_names(suffixes)
    write_suffixes(suffixes)

def write_suffix_names(the_set):
    logger.debug("entering write_sufffix_names (%s)", list)
    names = set()
    for x in the_set:
        names.add(x["name"])
    connQ = psycopg2.connect("dbname='poe_data'  user='poetools' password='monkey'")
    currQ = connQ.cursor()
    for x in names:
        try:
            currQ.execute("INSERT INTO suffix_names (name) "
                        "VALUES (%s)",
                       (x,))           
            connQ.commit()
        except psycopg2.IntegrityError:
            logger.info("psql integrity error when commiting suffix names (%s)", x)
            connQ.rollback() 

def write_suffixes(the_list):
    logger.debug("entering write_suffixes (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='poetools' password='monkey'")
    currQ = connQ.cursor()   
    for x in the_list:
        #print(x)
        currQ.execute("SELECT id FROM suffix_types WHERE type = (%s)", (x["type"],))
        suffix_type = currQ.fetchone()[0]
        currQ.execute("SELECT id FROM suffix_names WHERE name = (%s)", (x["name"],))
        name_id = currQ.fetchone()[0]
        for y in x["stats"]:
            #print(y)
            for keys, values in y.items():
                #print(keys, values)
                if "implicit_mod_key" in keys:
                    #print(values)
                    currQ.execute("SELECT id FROM stat_names WHERE name = (%s)", (values,))
                    name_id = currQ.fetchone()[0]
                if "min" in keys:
                    minimum = values
                if "max" in keys:
                    maximum = values
            currQ.execute("SELECT id FROM stats WHERE name_id = (%s) AND min_value = (%s) AND max_value = (%s)",
                          (name_id, minimum, maximum))
            stat_id = currQ.fetchone()[0]
            #print("data (%s)", (suffix_type, name_id, x["master_crafted"], stat_id))
            try:
                currQ.execute("INSERT INTO suffixes (type_id, name_id, i_level, crafted, stat) "
                              "VALUES (%s, %s, %s, %s, %s)",
                              (suffix_type, name_id, x["i_level"], str(x["master_crafted"]), stat_id,))           
                connQ.commit()
            except psycopg2.IntegrityError:
                logger.debug("psql integrity error when commiting suffixes (%s)", x)
                connQ.rollback() 
     
   
def fetch_weapons():
    weapon_types = []
    all_stats = set()
    all_weapons = []
    resp = s.get(url_weap)
    soup = BeautifulSoup(resp.text, 'html.parser')
    #print all weapon names
    weapons = soup.find_all("tr", {"class" : "even"}) 
    weapons[0].find_all("td", {"class": "name"})
    for y in weapons:
        a = y.find_all("td", {"class": "name"})
        #print (a[0].text) 
    all_items = soup.find_all("div", {"class": "layoutBox1 layoutBoxFull defaultTheme"})    
    for item_type in all_items:
        w_type = item_type.find_all("h1", {"class": "topBar last layoutBoxTitle"})[0].text #gets all item catagory names
        weapon_types.append(w_type)
        #write_weapon_types(weapon_types)
        items = item_type.find_all("table", {"class": "itemDataTable"}) #gets ALL the raw data for each item class
        for item_data in items: # for each weaspon class
            data = item_data.find_all("tr") #get the raw data
            x = 2 #first two entries are table formatting aspects
            while x < len(data): # need to collect two 'tr' entries for each item, so use while loop
                item_data = []
                item = {}
                raw_data = data[x].find_all("td")
                item["w_type"] = w_type
                item["large_url"] = raw_data[0].find_all("img")[0]["data-large-image"]
                item["small_url"] = raw_data[0].find_all("img")[0]["src"]
                item["name"] = raw_data[1].get_text()
                item["i_level"] = raw_data[2].get_text()
                #item["damage"] = raw_data[3].get_text()
                item["min_dmg"] = raw_data[3].get_text().split()[0]
                item["max_dmg"] = raw_data[3].get_text().split()[2]
                item["aps"] = raw_data[4].get_text()
                item["dps"] = raw_data[5].get_text()
                item["req_str"] = raw_data[6].get_text()
                item["req_dex"] = raw_data[7].get_text()
                item["req_int"] = raw_data[8].get_text()
                #urls = raw_data[0].find_all("img")
                #print("x, item", x, item)
                x = x+1                
                #implicits = data[x].find_all("td")
                #print("x, implicits ", x, implicits)
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
    write_weapon_types(weapon_types)
    write_weapon_names(all_weapons)
    write_weapon_stats(all_weapons)
    
def write_weapon_names(list):
    logger.debug("entering write_weapon_names (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='poetools' password='monkey'")
    currQ = connQ.cursor()  
    for x in list:
        try:
            pass
            currQ.execute("INSERT INTO weapon_names (name, w_type, i_level, min_dmg, max_dmg,"
                          "aps, dps, req_str, req_dex, req_int, large_url, small_url)"
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                          (x["name"], x["w_type"], x["i_level"], x["min_dmg"], x["max_dmg"],
                           x["aps"], x["dps"], x["req_str"], x["req_dex"], x["req_int"], x["large_url"],
                           x["small_url"],))           
            connQ.commit()
        except psycopg2.IntegrityError:
            logger.debug("psql integrity error when commiting weapon names (%s)", x)
            connQ.rollback() 

def write_weapon_stats(list):
    logger.debug("entering write_weapon_stats (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='poetools' password='monkey'")
    currQ = connQ.cursor()  
    for x in list:
        currQ.execute("SELECT id FROM weapon_names WHERE name = %s", (x["name"],))
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
                    currQ.execute("INSERT INTO weapon_stats (w_id, s_id) VALUES (%s, %s)",
                        (w_id, s_id,))           
                    connQ.commit()
                except psycopg2.IntegrityError:
                    logger.debug("psql integrity error when commiting weapon stats (%s)", x)
   
def fetch_clothes():
    clothes_types = []
    all_stats = set()
    all_clothes = []
    resp = s.get(url_clothes)
    soup = BeautifulSoup(resp.text, 'html.parser')
    #print all clothes names
    clothes = soup.find_all("tr", {"class" : "even"}) 
    clothes[0].find_all("td", {"class": "name"})
    for y in clothes:
        a = y.find_all("td", {"class": "name"})
        #print (a[0].text) 
    all_items = soup.find_all("div", {"class": "layoutBox1 layoutBoxFull defaultTheme"})    
    for item_type in all_items:
        c_type = item_type.find_all("h1", {"class": "topBar last layoutBoxTitle"})[0].text #gets all item catagory names
        clothes_types.append(c_type)
        #write_clothes_types(clothes_types)
        items = item_type.find_all("table", {"class": "itemDataTable"}) #gets ALL the raw data for each item class
        for item_data in items: # for each weaspon class
            data = item_data.find_all("tr") #get the raw data
            x = 2 #first two entries are table formatting aspects
            while x < len(data): # need to collect two 'tr' entries for each item, so use while loop
                #print(data[x])
                #input("Press Enter to continue...")
                item_data = []
                item = {}
                raw_data = data[x].find_all("td")
                item["c_type"] = c_type
                item["large_url"] = raw_data[0].find_all("img")[0]["data-large-image"]
                item["small_url"] = raw_data[0].find_all("img")[0]["src"]
                item["name"] = raw_data[1].get_text()
                item["i_level"] = raw_data[2].get_text()
                #item["damage"] = raw_data[3].get_text()
                item["armour"] = raw_data[3].get_text()
                item["evasion"] = raw_data[3].get_text()
                item["energy_shield"] = raw_data[4].get_text()
                item["req_str"] = raw_data[5].get_text()
                item["req_dex"] = raw_data[6].get_text()
                item["req_int"] = raw_data[7].get_text()
                #urls = raw_data[0].find_all("img")
                #print("x, item", x, item)
                x = x+1                
                #implicits = data[x].find_all("td")
                #print("x, implicits ", x, implicits)
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
                        #print("z, stop", z, stop)
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
                        #print("key_results, mod_values, a", key_results, ",", mod_values, ",", a)
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
    write_clothes_stats(all_clothes)
    
def write_clothes_names(list):
    logger.debug("entering write_clothes_names (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='poetools' password='monkey'")
    currQ = connQ.cursor()  
    for x in list:
        try:
            pass
            currQ.execute("INSERT INTO clothes_names (name, c_type, i_level, armour, evasion,"
                          "energy_shield, req_str, req_dex, req_int, large_url, small_url)"
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                          (x["name"], x["c_type"], x["i_level"], x["armour"], x["evasion"],
                           x["energy_shield"], x["req_str"], x["req_dex"], x["req_int"], x["large_url"],
                           x["small_url"],))           
            connQ.commit()
        except psycopg2.IntegrityError:
            logger.debug("psql integrity error when commiting clothes names (%s)", x)
            connQ.rollback() 

def write_clothes_stats(list):
    logger.debug("entering write_clothes_stats (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='poetools' password='monkey'")
    currQ = connQ.cursor()  
    for x in list:
        currQ.execute("SELECT id FROM clothes_names WHERE name = %s", (x["name"],))
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
                    currQ.execute("INSERT INTO clothes_stats (c_id, s_id) VALUES (%s, %s)",
                        (w_id, s_id,))           
                    connQ.commit()
                except psycopg2.IntegrityError:
                    logger.debug("psql integrity error when commiting clothes stats (%s)", x)

def fetch_jewelry():
    jewelry_types = []
    all_stats = set()
    all_jewelry = []
    resp = s.get(url_jewelry)
    soup = BeautifulSoup(resp.text, 'html.parser')
    #print all jewelry names
    jewelry = soup.find_all("tr", {"class" : "even"}) 
    jewelry[0].find_all("td", {"class": "name"})
    for y in jewelry:
        a = y.find_all("td", {"class": "name"})
        #print (a[0].text) 
    all_items = soup.find_all("div", {"class": "layoutBox1 layoutBoxFull defaultTheme"})    
    for item_type in all_items:
        j_type = item_type.find_all("h1", {"class": "topBar last layoutBoxTitle"})[0].text #gets all item catagory names
        jewelry_types.append(j_type)
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
                item["j_type"] = j_type
                item["large_url"] = raw_data[0].find_all("img")[0]["data-large-image"]
                item["small_url"] = raw_data[0].find_all("img")[0]["src"]
                item["name"] = raw_data[1].get_text()
                item["i_level"] = raw_data[2].get_text()      
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
    write_jewelry_types(jewelry_types)
    write_jewelry_names(all_jewelry)
    write_jewelry_stats(all_jewelry)
    
def write_jewelry_names(list):
    logger.debug("entering write_jewelry_names (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='poetools' password='monkey'")
    currQ = connQ.cursor()  
    for x in list:
        try:
            pass
            currQ.execute("INSERT INTO jewelry_names (name, j_type, i_level, large_url, small_url)"
                          "VALUES (%s, %s, %s, %s, %s)",
                          (x["name"], x["j_type"], x["i_level"], x["large_url"],x["small_url"],))           
            connQ.commit()
        except psycopg2.IntegrityError:
            logger.debug("psql integrity error when commiting jewelry names (%s)", x)
            connQ.rollback() 

def write_jewelry_stats(list):
    logger.debug("entering write_jewelry_stats (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='poetools' password='monkey'")
    currQ = connQ.cursor()  
    for x in list:
        currQ.execute("SELECT id FROM jewelry_names WHERE name = %s", (x["name"],))
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
                    currQ.execute("INSERT INTO jewelry_stats (j_id, s_id) VALUES (%s, %s)",
                        (w_id, s_id,))           
                    connQ.commit()
                except psycopg2.IntegrityError:
                    logger.debug("psql integrity error when commiting jewelry stats (%s)", x)

    

fetch_prefixes()
print(get_prefix_types("Armour"))
#fetch_suffixes()
#fetch_weapons()
#fetch_clothes()
#fetch_jewelry()

logger.info("Exiting POE Tools, it took "+str(datetime.datetime.now() - start_time))


