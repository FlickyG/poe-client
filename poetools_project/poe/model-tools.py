#!/bin/python

import poe.models as poe

#find all weapons with crit strike chance

crit = poe.StatNames.objects.filter(name = "Critical Strike Chance +%") #stat id 354

for x in crit:
    print(x.name)
    
#weapons = poe.WeaponStats.select_related.filter(poe.StatNames.objects.filter(name = "Critical Strike Chance +%")[0].id)

weapons = WeaponStats.objects.select_related()

### this returns all the stats with id = 354
data = Stats.objects.select_related()
stat_id = data.filter(name = 354)
'''>>> for x in stat_id:
...     print(x.id)
... 
1879
1884
1887
1894
1906
1909
2073
2093
2107
2168
2174
2183
2197
2204
2206
2234
2263
2280
2281
2312
2410
2430'''

####
#list of weapon ids for given stat ids, where the stat name is critical strike
##

b = [int(i[0]) for i in weapons.filter(s__id__in = stat_id).values_list("w_id")]
weaps = WeaponNames.objects.filter(id__in = b)
for x in weaps:
    print(x.name)
####

crit = poe.StatNames.objects.get(name = "Weapon Elemental Damage +%").id

y = "Weapon Elemental Damage +%"
data = Stats.objects.select_related().filter(name = poe.StatNames.objects.get(name = y).id)

weapons = WeaponStats.objects.select_related()
b = [int(i[0]) for i in weapons.filter(s__id__in = data).values_list("w_id")]
weaps = WeaponNames.objects.filter(id__in = b)
for x in weaps:
    print(x.name)



