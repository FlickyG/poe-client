#!/bin/python

import poe.models as poe

y = "Weapon Elemental Damage +%"

# get the stat ids for a given stat name
def get_stat_ids_from_stat_name(stat_name):
    crit = poe.StatNames.objects.get(name = stat_name).id
    data = poe.Stats.objects.select_related().filter(name = crit)
    return data #stats

# get the weapon names from     
def get_weapons_from_stat_name(stat_name_string):
    data = poe.Stats.objects.select_related().filter(
        name = poe.StatNames.objects.get(name = stat_name_string)
        .id)
    weapons = poe.WeaponStats.objects.select_related()
    b = [int(i[0]) for i in weapons.filter(s__id__in = data).values_list("w_id")]
    weaps = poe.WeaponNames.objects.filter(id__in = b)
    return weaps
    
for x in data:
    print(x.name)

#get stats from stat name string
d = get_stat_ids_from_stat_name("Weapon Elemental Damage +%")
for x in d:
    print (x.name)


d = get_stat_ids_from_stat_name("Additional Intelligence")
for x in d:
    print (x.name)

def get_suffix_names_from_stat_id(id):

