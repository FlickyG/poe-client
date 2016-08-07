#!/bin/python3
#import urllib.request, xmltodict
import time, requests, requests_cache
from bs4 import BeautifulSoup

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
    if item_data[1][0].get_text():
        item["implicit_mod"] = item_data[1][0].get_text()
        #print (item["implicit_mod"])
        item["min_implicit_value"] = item_data[1][1].get_text().split()[0]
        if len(item_data[1][1].get_text().split()) > 1:
            item["max_implicit_value"] = item_data[1][1].get_text().split()[2]
        else:
            item["max_implicit_value"] = item_data[1][1].get_text().split()[0]
    return item
    
        
def parse_clothing(data):
    item = {}
    item["large_url"] = item_data[0][0].find_all("img")[0]["data-large-image"]
    item["small_url"] = item_data[0][0].find_all("img")[0]["src"]
    item["name"] = item_data[0][1].get_text()
    item["item_level"] = item_data[0][2].get_text()

    #print (item)

requests_cache.install_cache('first_go', expires_after = 1)
requests_cache.clear()
s =  requests.Session()
s.hooks = {'response': make_throttle_hook(0.1)}

url_weap = "https://www.pathofexile.com/item-data/weapon"
url_clothes = "http://www.pathofexile.com/item-data/armour"

def get_weapons():
    resp = s.get(url_weap)
    soup = BeautifulSoup(resp.text, 'html.parser')
    #print all weapon names
    weapons = soup.find_all("tr", {"class" : "even"}) 
    weapons[0].find_all("td", {"class": "name"})
    for y in weapons:
        a = y.find_all("td", {"class": "name"})
        #print (a[0].text)
    print ("### END OF PRINTIONG ALL WEAPON NAMES ###")
        
    all_items = soup.find_all("div", {"class": "layoutBox1 layoutBoxFull defaultTheme"})
    
    #print all item typyes
    for item_type in all_items:
        w_type = item_type.find_all("h1", {"class": "topBar last layoutBoxTitle"})[0].text #gets all item catagory names
        items = item_type.find_all("table", {"class": "itemDataTable"}) #gets ALL the raw data for each item class
        print("len of items", len(items))
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
                parse_weapon(item_data)
                x = x+1

def get_clothes():
    resp = s.get(url_clothes)
    soup = BeautifulSoup(resp.text, 'html.parser')
    #print all clotheson names
    clothes = soup.find_all("tr") 
    clothes[0].find_all("td", {"class": "name"})
    for y in clothes:
        a = y.find_all("td", {"class": "name"})
        if len(a) > 0:
            print (a[0].text)
    print ("### END OF PRINTIONG ALL WEAPON NAMES ###")
        
    all_items = soup.find_all("div", {"class": "layoutBox1 layoutBoxFull defaultTheme"})
    
    #print all item typyes
    for item_type in all_items:
        c_type = item_type.find_all("h1", {"class": "topBar last layoutBoxTitle"})[0].text #gets all item catagory names
        items = item_type.find_all("table", {"class": "itemDataTable"}) #gets ALL the raw data for each item class
        #print ("type items ", type(items))
        for item_data in items: # for each clothing class
            data = item_data.find_all("tr") #get the raw data
            x = 2 #first two entries are table formatting aspects
            #print ("length of data", len(data))
            while x < len(data): # need to collect two 'tr' entries for each item, so use while loop
                item_data = []
                raw_data = data[x].find_all("td")
                item_data.append(raw_data)
                #urls = raw_data[0].find_all("img")
                x = x+1
                implicits = data[x].find_all("td")
                item_data.append(implicits)
                print ("IMPS", implicits)
                parse_clothing(item_data)
                x = x+1
                #input("Press Enter to continue...")
    
    #"itemDataIcon" in urls[0]["class"][0]
    #urls[0]["class"][0]

get_weapons()


