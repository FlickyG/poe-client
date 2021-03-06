#!/bin/Python26DeprecationWarning
import django_tables2 as tables
import poe.models

import logging
stdlogger = logging.getLogger(__name__)
stdlogger.debug("Entering poe.tabels")


class ItemTable(tables.Table):
    class Meta:
        model = poe.models.ItemName
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
                    'len_stats',                    
                )
        attrs = {'width':'100%'}        
        
class WeaponTable(tables.Table):
    class Meta:
        model = poe.models.ItemName
        #stdlogger.debug("ItemName.type", poe.models.ItemName.type)
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
                    #'len_stats',
                    'stat_names', 
                )
        attrs = {'width':'100%'}
        
class ClothingTable(tables.Table):
    class Meta:
        model = poe.models.ItemName
        fields = (
                    'name',
                    'i_level',
                    'req_str',
                    'req_dex',
                    'req_int',
                    'armour',
                    'evasion',
                    'energy_shield',
                    'len_stats',
                    'stat_names',                   
                )
        attrs = {'width':'100%'}        
        
class JewelTable(tables.Table):
    class Meta:
        model = poe.models.ItemName
        stat_name = tables.Column()
        fields = (
                    'name',
                    'i_level',
                    'len_stats',
                    'stat_names',                    
                )
        
        
class CharTable(tables.Table):
    class Meta:
        model = poe.models.PoeCharacter
        fields = (
                  'name',
                  'ggg_class',
                  'league',
                  'level',
                  )
        attrs = {'width':'100%'}