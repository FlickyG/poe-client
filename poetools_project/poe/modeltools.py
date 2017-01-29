#!/bin/python

import poe.models as poe
from django.db.models.query import QuerySet
from pprint import PrettyPrinter

y = "Weapon Elemental Damage +%"

# print queryset
def dprint(object, stream=None, indent=1, width=80, depth=None):
    """
    A small addition to pprint that converts any Django model objects to dictionaries so they print prettier.

    h3. Example usage

        >>> from toolbox.dprint import dprint
        >>> from app.models import Dummy
        >>> dprint(Dummy.objects.all().latest())
         {'first_name': u'Ben',
          'last_name': u'Welsh',
          'city': u'Los Angeles',
          'slug': u'ben-welsh',
    """
    # Catch any singleton Django model object that might get passed in
    if getattr(object, '__metaclass__', None):
        if object.__metaclass__.__name__ == 'ModelBase':
            # Convert it to a dictionary
            object = object.__dict__
    
    # Catch any Django QuerySets that might get passed in
    elif isinstance(object, QuerySet):
        # Convert it to a list of dictionaries
        object = [i.__dict__ for i in object]
        
    # Pass everything through pprint in the typical way
    printer = PrettyPrinter(stream=stream, indent=indent, width=width, depth=depth)
    printer.pprint(object)

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

def get_suffix_names_from_stat_id(id):
    # accepts list of indexes from the stat table
    # returns unique list of names of the prefixes that match the stat ids 
    p = poe.Prefixes.objects.filter(stat__id__in = id)
    p_list = [int(i[0]) for i in p.values_list("name_id")]
    pn = poe.PrefixNames.objects.filter(id__in = p_list).values_list("name")
    return sorted(set([(i[0]) for i in pn]))


d = get_stat_ids_from_stat_name("Weapon Elemental Damage +%")
stat_list = [int(i[0]) for i in d.values_list("id")]
get_suffix_names_from_stat_id(stat_list)

'''
d = get_stat_ids_from_stat_name("Local Armour And Energy Shield +%")
stat_list = [int(i[0]) for i in d.values_list("id")]
get_suffix_names_from_stat_id(stat_list)

'''
for z in models.Fix.objects.select_related().filter(name_id__type_id__name = "Armour"):
    print(z.name.name, z.stat.min_value, z.stat.max_value)

z = models.Fix.objects.select_related().filter(name_id__name = "Essences")
for x in z:
    print(x.id, x.name.type.name, x.name.name, x.name.type.category.name)


# get weapon id for a weapon with a name
#weapon_id = poe.WeaponNames.objects.filter(name = "Death Bow")[0].id
#8
#get weapon stats for the Death Bow 
#data = poe.WeaponStats.objects.select_related().filter(w_id__name = "Death Bow")[0].s_id
# get stats for stat-id
# mystats = poe.Stats.objects.select_related().filter(id = data)[0].name_id
# get stat names from stat id
# stat_name = poe.StatNames.objects.select_related().filter(id = mystats)

data = poe.WeaponStats.objects.select_related().filter(w_id__name = "Nailed Fist")[0].s_id
mystats = poe.Stats.objects.select_related().filter(id = data)[0].name_id
stat_name = poe.StatNames.objects.select_related().filter(id = mystats)
stat_name[0].name

UserFollows.objects.filter(profile_id=12345).select_related(‌​'profile', 'following')