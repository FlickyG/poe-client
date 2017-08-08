from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse 
from . import models
#from . import modeltools as poe2
# Create your tests here.

class SimpleTestCase(TestCase):
    '''def test_registration(self):
        url = reverse("registration_register")
        response = self.client.post(url, {
            "username":'mike2001',
            "password1":"password123",
            "password2":"password123",
            "poe_sessid": "lkjhkjh23",
            "poe_account_name": "mikesaccount",
            "email": "s@s.com"
        })
        #self.assertEqual(response.status_code, 302) 
        models.PoeUser.objects.get(username = "mike2001")
        session = self.client.session
        '''
   
    def test_index_page(self):
        url = reverse("index")
        response = self.client.post(url)
        self.assertIn(b'<h1>Flicky says... hello world!</h1>', response.content)

    def test_registration_login(self):
        url = reverse("registration_register")
        response = self.client.post(url, {
            "username":'mike2001',
            "password1":"password123",
            "password2":"password123",
            "poe_sessid": "12345678901234567890123456789012",
            "poe_account_name": "mikesaccount",
            "email": "s@s.com"
        })
        self.assertEqual(response.status_code, 302) 
        models.PoeUser.objects.get(username = "mike2001")
        session_key = self.client.session.session_key
        ####
        url = reverse('index')
        print("url", url)
        response = self.client.post(url, {"new_sessid" :'sdsdsdsd'})
        self.assertEqual(response.status_code, 200)
        print("sessid resp", response)
        
    def test_registration_set_sessid(self):
        url = reverse("registration_register")
        response = self.client.post(url, {
            "username":'mike2001',
            "password1":"password123",
            "password2":"password123",
            "poe_sessid": "12345678901234567890123456789012",
            "poe_account_name": "mikesaccount",
            "email": "s@s.com"
        })
        self.assertEqual(response.status_code, 302) 
        models.PoeUser.objects.get(username = "mike2001")
        session_key = self.client.session.session_key
        ####
        url = reverse('index')
        print("url", url)
        response = self.client.post(url, {"new_sessid" :'sdsdsdsd'})
        self.assertEqual(response.status_code, 200)
        print("sessid resp", response)

                
    def test_login(self):
        url = reverse("registration_register")
        response = self.client.post(url, {
            "username":'mike2001',
            "password1":"password123",
            "password2":"password123",
            "poe_sessid": "12345678901234567890123456789012",
            "poe_account_name": "mikesaccount",
            "email": "s@s.com"
        })
        url= '/accounts/login/'
        response = self.client.post(url, {"username": "mike2001",
                                          "password" :'password123'})
        print(response, " ", response.status_code)
        self.assertEqual(response.status_code, 302) # login worked!
        

class GenericDataTableLengths(TestCase):
    print("GenericDataTestCase")
    multi_db = True
    fixtures = ["poe/fixtures/dumpdata.yaml",]

    def test_suffix_names(self):
        print("GenericDataTestCase")
        crit = models.StatNames.objects.all() #get(name = "Weapon Elemental Damage +%").id

### Prefixes
    def test_length_prefix_types(self):
        #length of prefix_types =  33
        data = models.FixType.objects.select_related().filter(category_id__name = "Prefix")
        self.assertEqual(len(data), 33)
        
    def test_length_prefix_names(self):
        #length of prefix names  480, raised to 484 on r2.6
        data = models.FixName.objects.select_related().filter(type_id__category_id__name = "Prefix")
        self.assertEqual(len(data), 484)
   
    def test_length_prefixes(self):
        #length of prefixes 1035, raised to 1042 a r2.6
        #length of z once the inner stat dictionary of the higher list is known
        data = models.Fix.objects.select_related().filter(name_id__type_id__category_id__name = "Prefix")
        self.assertEqual(len(data), 1042)
## Suffixes      
    def test_length_suffix_types(self):
        #length of suffix_types =  24
        data = models.FixType.objects.select_related().filter(category_id__name = "Suffix")
        self.assertEqual(len(data), 24)
        
    def test_length_suffix_names(self):
        #length of suffix names 270
        data = models.FixName.objects.select_related().filter(type_id__category_id__name = "Suffix")
        self.assertEqual(len(data), 270)
   
    def test_length_suffixes(self):
        #length of suffixes 420
        #length of z once the inner stat dictionary of the higher list is known
        data = models.Fix.objects.select_related().filter(name_id__type_id__category_id__name = "Suffix")
        self.assertEqual(len(data), 420)

## weapons
    def test_length_weapon_names(self):
        #length of weapon names 307
        data = models.ItemName.objects.select_related().filter(type_id__type_id__name = "Weapons")
        self.assertEqual(len(data), 307)

    def test_length_weapon_stats(self):
        #length of weapon stats 250, rasied to 253 at r2.6
        data = models.ItemStat.objects.select_related().filter(i_id__type_id__type_id__name = "Weapons")
        self.assertEqual(len(data), 253)

## clothes
    def test_length_clothes_names(self):
        #length of clothes names 362
        data = models.ItemName.objects.select_related().filter(type_id__type_id__name = "Clothes")
        self.assertEqual(len(data), 362)

    def test_length_clothes_stats(self):
        #length of clothesweapon stats 244
        data = models.ItemStat.objects.select_related().filter(i_id__type_id__type_id__name = "Clothes")
        self.assertEqual(len(data), 244)

## jewelry
    def test_length_jewelry_names(self):
        #length of jewelry names 74
        data = models.ItemName.objects.select_related().filter(type_id__type_id__name = "Jewelry")
        self.assertEqual(len(data), 65 )

    def test_length_jewelry_stats(self):
        #length of jewelry stats 111
        data = models.ItemStat.objects.select_related().filter(i_id__type_id__type_id__name = "Jewelry")
        self.assertEqual(len(data), 111)

## Stats
    def test_length_stats(self):
        #length of stats  1515 (sued to be 1530 before model reduction)
        #raised to 1548 at r2.6
        data = models.Stats.objects.all()
        self.assertEqual(len(data), 1548)
        
    def test_length_stat_names(self):
        #length of stat_names 266
        #length of z once the inner stat dictionary of the higher list is known
        data = models.StatNames.objects.all()
        self.assertEqual(len(data), 266)

class GenericDataTableContents(TestCase):
    print("GenericDataTablecontents")
    multi_db = True
    fixtures = ["poe/fixtures/dumpdata.yaml",]
    
    def test_category_type(self):
        data = models.ItemCategory.objects.all()
        names = []
        for x in data:
            names.append(x.name)
        names.sort()
        self.assertListEqual(names, ['Clothes', 'Jewelry', 'Weapons'])

    def test_item_types(self):
        data = models.ItemType.objects.all()
        names = []
        for x in data:
            names.append(x.name)
        names.sort()
        self.assertListEqual(names, [
            'Amulet', 'Belt', 'Body Armour', 'Boots', 'Bow', 'Claw', 'Dagger', 
            'Gloves', 'Helmet', 'One Hand Axe', 'One Hand Mace', 
            'One Hand Sword', 'Ring', 'Sceptre', 'Shield', 'Staff', 
            'Thrusting One Hand Sword', 'Two Hand Axe', 'Two Hand Mace', 
            'Two Hand Sword', 'Wand'])
        
    def test_weapon_stat(self):
        data = models.ItemStat.objects.select_related().filter(i_id__name = "Highborn Bow")
        self.assertEqual(data[0].i.min_dmg, 17)
        self.assertEqual(data[0].i.max_dmg, 66)
        self.assertEqual(data[0].i.i_level, 50)
        self.assertEqual(data[0].s.name.name, "Weapon Elemental Damage +%")
        self.assertEqual(data[0].s.min_value, 20)
        self.assertEqual(data[0].s.max_value, 24)
        #
        data = models.ItemStat.objects.select_related().filter(i_id__name = "Blinder")
        self.assertEqual(data[0].i.i_level, 22)
        self.assertEqual(data[0].i.min_dmg, 12)
        self.assertEqual(data[0].i.max_dmg, 32)
        self.assertEqual(data[0].s.name.name, "Local Life Gain Per Target")
        self.assertEqual(data[0].s.min_value, 12)
        self.assertEqual(data[0].s.max_value, 12)
        #
        data = models.ItemStat.objects.select_related().filter(i_id__name = "Etched Hatchet")
        self.assertEqual(data[0].i.min_dmg, 26)
        self.assertEqual(data[0].i.max_dmg, 46)
        self.assertEqual(data[0].i.i_level, 35)
        self.assertEqual(data[0].s.name.name, "Physical Damage +%")
        self.assertEqual(data[0].s.min_value, 8)
        self.assertEqual(data[0].s.max_value, 8)

    def test_cloth_stat(self):
        data = models.ItemStat.objects.select_related().filter(i_id__name = "Plate Vest")
        self.assertEqual(data[0].i.evasion, 0)
        self.assertEqual(data[0].i.armour, 14)
        self.assertEqual(data[0].i.energy_shield, 0)
        self.assertEqual(data[0].s.name.name, "From Armour Movement Speed +%")
        self.assertEqual(data[0].s.min_value, -3)
        self.assertEqual(data[0].s.max_value, -3)
        
        data = models.ItemStat.objects.select_related().filter(i_id__name = "Two-Toned Boots")
        self.assertEqual(data[0].i.i_level, 72)
        self.assertEqual(data[0].i.evasion, 109)
        self.assertEqual(data[0].i.armour, 0)
        self.assertEqual(data[0].i.energy_shield, 32)
        self.assertEqual(data[0].s.name.name, "Cold And Lightning Damage Resistance %")
        self.assertEqual(data[0].s.min_value, 15)
        self.assertEqual(data[0].s.max_value, 20)

    def test_jewelry_stat(self):
        data = models.ItemStat.objects.select_related().filter(i_id__name = "Golden Obi")
        self.assertEqual(data[0].i.i_level, 12)
        self.assertEqual(data[0].i.evasion, None)
        self.assertEqual(data[0].i.armour, None)
        self.assertEqual(data[0].i.energy_shield, None)
        self.assertEqual(data[0].s.name.name, "Base Item Found Rarity +%")
        self.assertEqual(data[0].s.min_value, 20)
        self.assertEqual(data[0].s.max_value, 30)
        
        data = models.ItemStat.objects.select_related().filter(i_id__name = "Longtooth Talisman")
        self.assertEqual(data[0].i.i_level, 1)
        self.assertEqual(data[0].i.evasion, None)
        self.assertEqual(data[0].i.armour, None)
        self.assertEqual(data[0].i.energy_shield, None)
        #
        stat1 = data.filter(s_id__name_id__name = "Base Additional Physical Damage Reduction %")[0]
        self.assertEqual(stat1.s.name.name, "Base Additional Physical Damage Reduction %")
        self.assertEqual(stat1.s.min_value, 4)
        self.assertEqual(stat1.s.max_value, 6)
        #
        stat2 = data.filter(s_id__name_id__name = "Local Stat Monsters Pick Up Item")[0]
        self.assertEqual(stat2.s.name.name, "Local Stat Monsters Pick Up Item")
        self.assertEqual(stat2.s.min_value, 1)
        self.assertEqual(stat2.s.max_value, 1)

    def test_index_page(self):
        url = reverse("index")
        response = self.client.post(url)
        self.assertIn(b'<li  class="list-group-item"><a href="/poe/item/weapons/">Weapons</a></li>', response.content)
        self.assertIn(b'<li  class="list-group-item"><a href="/poe/item/weapons/">Weapons</a></li>', response.content)
        self.assertIn(b'<li  class="list-group-item"><a href="/poe/item/jewelry/">Jewelry</a></li>', response.content)
        self.assertIn(b'<li  class="list-group-item"><a href="/poe/mods/prefix/">Prefix</a></li>', response.content)
        self.assertIn(b'<li  class="list-group-item"><a href="/poe/mods/suffix/">Suffix</a></li>', response.content)
        

    def test_assert_lists(self):
        a = ["dave", "adam", "clive"]
        a.sort()
        self.assertListEqual(a, ["adam", "clive", "dave"])
