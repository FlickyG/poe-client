#!/bin/python3
#import urllib.request, xmltodict
import time, requests, requests_cache
from bs4 import BeautifulSoup
import re
from email._header_value_parser import Section
import psycopg2
import logging, logging.config
import sys #for excepotion handling and printing

logging.config.fileConfig('poe_tools_logging.conf')
logger = logging.getLogger(__name__)
logger.debug("hello world")
print(__name__)

def write_weapon_types(list):
    logger.debug("entering write_weapon_types (%s)", list)
    connQ = psycopg2.connect("dbname='poe_data'  user='adam' password='green'")
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
    connQ = psycopg2.connect("dbname='poe_data'  user='adam' password='green'")
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
    connQ = psycopg2.connect("dbname='poe_data'  user='adam' password='green'")
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
    connQ = psycopg2.connect("dbname='poe_data'  user='adam' password='green'")
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
    connQ = psycopg2.connect("dbname='poe_data'  user='adam' password='green'")
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


def parse_weapon(item_data):
    item = {}
    # standard parameters accross all items
    item["large_url"] = item_data[0][0].find_all("img")[0]["data-large-image"]
    item["small_url"] = item_data[0][0].find_all("img")[0]["src"]
    item["name"] = item_data[0][1].get_text()
    item["item_level"] = item_data[0][2].get_text()
    #item["damage"] = item_data[0][3].get_text()
    item["min_dmg"] = item_data[0][3].get_text().split()[0]
    item["max_dmg"] = item_data[0][3].get_text().split()[2]
    item["attacks_per_second"] = item_data[0][4].get_text()
    item["dps"] = item_data[0][5].get_text()
    item["req_str"] = item_data[0][6].get_text()
    item["req_dex"] = item_data[0][7].get_text()
    item["req_int"] = item_data[0][8].get_text()
    # implicit aspects
    try:
        item_data[1][0].get_text()
        item["implicit_mod"] = item_data[1][0].get_text()
        #print (item["implicit_mod"])
        item["min_implicit_value"] = item_data[1][1].get_text().split()[0]
        if len(item_data[1][1].get_text().split()) > 1:
            item["max_implicit_value"] = item_data[1][1].get_text().split()[2]
        else:
            item["max_implicit_value"] = item_data[1][1].get_text().split()[0]
        return item
    except IndexError:
        pass   
    
        
def parse_clothing(item_data):
    item = {}
    item["large_url"] = item_data[0][0].find_all("img")[0]["data-large-image"]
    item["small_url"] = item_data[0][0].find_all("img")[0]["src"]
    item["name"] = item_data[0][1].get_text()
    item["item_level"] = item_data[0][2].get_text()
    item["armour"] = item_data[0][3].get_text()
    item["evasion_rating"] = item_data[0][4].get_text()
    item["energy_shield"] = item_data[0][5].get_text()
    item["required_str"] = item_data[0][6].get_text()
    item["req_dex"] = item_data[0][6].get_text()
    item["req_int"] = item_data[0][6].get_text()
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
      

def parse_prefixes(item_data):
    #item_data [[<td class="name">Electrocuting</td>, <td>74</td>, <td>Spell Minimum Added Lightning Damage<br/>Spell Maximum Added Lightning Damage</td>, <td>5 to 15<br/>189 to 200</td>]]
    #top of while loop
    #item_data [[<td class="name">Catalysing</td>, <td>4</td>, <td>Weapon Elemental Damage +%</td>, <td>5 to 10</td>]]
    item = {}
    if '(Master Crafted)' in item_data[0][0].get_text():
        item["name"] = item_data[0][0].get_text().split("(Master Crafted)")[0]
        item['master_crafted'] = True
    else:
        item["name"] = item_data[0][0].get_text()
        item['master_crafted'] = False
    item["name"] = item_data[0][0].get_text()
    item["level"] = item_data[0][1].get_text()
    mods = [ x for x in re.findall(r">(.*?)<",str(item_data[0][2:])) if (x and ((x != ", ") or (x != ", ")))]
    assert len(mods)%2 == 0
    stop = int(len(mods)/2) #NEED TO ROUN THIS UP
    #print("stop", stop, mods)
    key_results = mods[:stop]
    values_results = mods[stop:]
    assert len(key_results) == len(values_results)
    mod_keys = []
    mod_values = []
    for x in values_results:
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
        number_of_mods = len(these_values)
        #print("number_of_mods", number_of_mods, mod_values) #NOT GETTING THE SECOND SET
    for x in range(0,stop):   
        item["implicit_mod_key_"+str(x)] = key_results[x]
        item["implicit_mod_values_"+str(x)+"_min"] = mod_values[x][0]
        item["implicit_mod_values_"+str(x)+"_max"] = mod_values[x][1]
    return(item)
        
def parse_suffixes(item_data):
    #item_data [[<td class="name">Electrocuting</td>, <td>74</td>, <td>Spell Minimum Added Lightning Damage<br/>Spell Maximum Added Lightning Damage</td>, <td>5 to 15<br/>189 to 200</td>]]
    #top of while loop
    #item_data [[<td class="name">Catalysing</td>, <td>4</td>, <td>Weapon Elemental Damage +%</td>, <td>5 to 10</td>]]
    item = {}
    if '(Master Crafted)' in item_data[0][0].get_text():
        item["name"] = item_data[0][0].get_text().split("(Master Crafted)")[0]
        item['master_crafted'] = True
    else:
        item["name"] = item_data[0][0].get_text()
        item['master_crafted'] = False
    item["level"] = item_data[0][1].get_text()
    mods = [ x for x in re.findall(r">(.*?)<",str(item_data[0][2:])) if (x and ((x != ", ") or (x != ", ")))]
    assert len(mods)%2 == 0
    stop = int(len(mods)/2)
    key_results = mods[:stop]
    values_results = mods[stop:]
    assert len(key_results) == len(values_results)
    mod_keys = []
    mod_values = []
    for x in values_results:
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
        number_of_mods = len(these_values)-1
        for x in range(0,number_of_mods):
            item["implicit_mod_values_"+str(x)+"_min"] = mod_values[x][0]
            item["implicit_mod_values_"+str(x)+"_max"] = mod_values[x][1]

def fetch_weapons():
    weapon_types = []
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
                raw_data = data[x].find_all("td")
                item_data.append(raw_data)
                #urls = raw_data[0].find_all("img")
                x = x+1
                implicits = data[x].find_all("td")
                item_data.append(implicits)
                item = parse_weapon(item_data)
                x = x+1
    write_weapon_types(weapon_types)

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
    connQ = psycopg2.connect("dbname='poe_data'  user='adam' password='green'")
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
    
def write_prefix(p_type, prefix):
    print("entering prefixes", p_type, prefix)
    connQ = psycopg2.connect("dbname='poe_data'  user='adam' password='green'")
    currQ = connQ.cursor()
    try:
        pass
    except:
        print("entering exception case in write_prefix_types", sys.exc_info()[0])
    
def fetch_prefixes_types(): #layout is different - implicit mods are on the same line
    prefix_types = []
    prefixes = []
    resp = s.get(url_prefixes)
    soup = BeautifulSoup(resp.text, 'html.parser')
    prefixes = soup.find_all("tr") 
    prefixes[0].find_all("td", {"class": "name"})
    for y in prefixes:
        a = y.find_all("td", {"class": "name"})
        if len(a) > 0:
            pass
    all_items = soup.find_all("div", {"class": "layoutBox1 layoutBoxFull defaultTheme"})
    for item_type in all_items:
        p_type = item_type.find_all("h1", {"class": "topBar last layoutBoxTitle"})[0].text #gets all item catagory names
        prefix_types.append(p_type)
    write_prefix_types(prefix_types)

def fetch_prefixes(): #layout is different - implicit mods are on the same line
    prefix_types = []
    prefixes = []
    resp = s.get(url_prefixes)
    soup = BeautifulSoup(resp.text, 'html.parser')
    prefixes = soup.find_all("tr") 
    prefixes[0].find_all("td", {"class": "name"})
    for y in prefixes:
        a = y.find_all("td", {"class": "name"})
        if len(a) > 0:
            pass
    all_items = soup.find_all("div", {"class": "layoutBox1 layoutBoxFull defaultTheme"})
    for item_type in all_items:
        p_type = item_type.find_all("h1", {"class": "topBar last layoutBoxTitle"})[0].text #gets all item catagory names
        prefix_types.append(p_type)
        items = item_type.find_all("table", {"class": "itemDataTable"}) #gets ALL the raw data for each item class
        for item_data in items: # for each clothing class
            data = item_data.find_all("tr") #get the raw data
            x = 1 #first two entries are table formatting aspects
            while x < len(data): # need to collect two 'tr' entries for each item, so use while loop
                item_data = []
                raw_data = data[x].find_all("td")
                item_data.append(raw_data)
                #prefix = parse_prefixes(item_data)
                #write_prefix(get_prefix_types(p_type), prefix)
                x = x+1
    
                
def fetch_prefix_stats(): #layout is different - implicit mods are on the same line
    all_the_stats = set()
    xxx = []
    prefixes = []
    resp = s.get(url_prefixes)
    soup = BeautifulSoup(resp.text, 'html.parser')
    prefixes = soup.find_all("tr") 
    prefixes[0].find_all("td", {"class": "name"})
    for y in prefixes:
        a = y.find_all("td", {"class": "name"})
        if len(a) > 0:
            pass
    all_items = soup.find_all("div", {"class": "layoutBox1 layoutBoxFull defaultTheme"})
    for item_type in all_items:
        items = item_type.find_all("table", {"class": "itemDataTable"}) #gets ALL the raw data for each item class
        for each_class in items: # for each prefix class
            data = each_class.find_all("tr") #get the raw data
            y = 1 #first two entries are table formatting aspects
            while y < len(data): # need to collect two 'tr' entries for each item, so use while loop
                item_data = []
                raw_data = data[y].find_all("td")
                item_data.append(raw_data)
                #prefix = parse_prefixes(item_data)
                mods = [ z for z in re.findall(r">(.*?)<",str(item_data[0][2:])) if (z and ((z != ", ") or (z != ", ")))]
                assert len(mods)%2 == 0
                stop = int(len(mods)/2) #NEED TO ROUN THIS UP
                key_results = mods[:stop]
                values_results = mods[stop:]
                assert len(key_results) == len(values_results)
                mod_keys = []
                mod_values = []
                for x in values_results:
                    #print(x) 
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
                    number_of_mods = len(these_values)
                for x in range(0,stop):
                    test_stat = {}
                    test_stat["implicit_mod_key_"+str(x)] = key_results[x]
                    test_stat["implicit_mod_values_"+str(x)+"_min"] = mod_values[x][0]
                    test_stat["implicit_mod_values_"+str(x)+"_max"] = mod_values[x][1]
                    all_the_stats.add((key_results[x], mod_values[x][0], mod_values[x][1])) #use tuples as ordered and hashable
                    #all_the_stats.update(test_stat)
                y = y+1
    print(all_the_stats)
    WE HAVE ALL THE STATS NOW NEED TO WRITE THEM TO DB
    
def fetch_suffixes(): #layout is different - implicit mods are on the same line
    suffix_types = []
    resp = s.get(url_suffixes)
    soup = BeautifulSoup(resp.text, 'html.parser')
    suffixes = soup.find_all("tr") 
    suffixes[0].find_all("td", {"class": "name"})
    for y in suffixes:
        a = y.find_all("td", {"class": "name"})
        if len(a) > 0:
            pass
            #print (a[0].text)
    all_items = soup.find_all("div", {"class": "layoutBox1 layoutBoxFull defaultTheme"})
    for item_type in all_items:
        s_type = item_type.find_all("h1", {"class": "topBar last layoutBoxTitle"})[0].text #gets all item catagory names
        suffix_types.append(s_type)
        items = item_type.find_all("table", {"class": "itemDataTable"}) #gets ALL the raw data for each item class
        for item_data in items: # for each clothing class
            data = item_data.find_all("tr") #get the raw data
            x = 1 #first two entries are table formatting aspects
            while x < len(data): # need to collect two 'tr' entries for each item, so use while loop
                item_data = []
                raw_data = data[x].find_all("td")
                item_data.append(raw_data)
                parse_suffixes(item_data)
                x = x+1
    write_suffix_types(suffix_types)     
 
#fetch_prefixes_types()
#fetch_prefixes()
fetch_prefix_stats()
print(get_prefix_types("Armour"))
#fetch_suffixes()
#fetch_weapons()
#fetch_clothes()
#fetch_jewelry()


