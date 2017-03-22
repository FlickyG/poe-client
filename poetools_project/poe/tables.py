#!/bin/Python26DeprecationWarning
import django_tables2 as tables
import poe.models

class ItemTable(tables.Table):
    class Meta:
        model = poe.models.ItemName
        print("ItemName.type", poe.models.ItemName.type)
        fields = (
                    'name',
                    'i_level',
                    'min_dmg',
                    'max_dmg',
                    'aps',
                    'dps',
                    'req_str',
                    'req_dex',
                    'req_int',
                    'armour',
                    'evasion',
                    'energy_shield',
                )
        
class WeaponTable(tables.Table):
    class Meta:
        model = poe.models.ItemName
        print("ItemName.type", poe.models.ItemName.type)
        fields = (
                    'name',
                    'i_level',
                    'min_dmg',
                    'max_dmg',
                    'aps',
                    'dps',
                    'req_str',
                    'req_dex',
                    'req_int',
                    'stats.name',
                )
        attrs = {'width':'100%'}
        
class ClothingTable(tables.Table):
    class Meta:
        model = poe.models.ItemName
        print("ItemName.type", poe.models.ItemName.type)
        fields = (
                    'name',
                    'i_level',
                    'req_str',
                    'req_dex',
                    'req_int',
                    'armour',
                    'evasion',
                    'energy_shield',
                )
        
class JewelTable(tables.Table):
    class Meta:
        model = poe.models.ItemName
        print("ItemName.type", poe.models.ItemName.type)
        fields = (
                    'name',
                    'i_level',
                    'min_dmg',
                    'max_dmg',
                    'aps',
                    'dps',
                    'req_str',
                    'req_dex',
                    'req_int',
                    'armour',
                    'evasion',
                    'energy_shield',
                )