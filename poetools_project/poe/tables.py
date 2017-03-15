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