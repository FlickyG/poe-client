from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse 
from . import models
#from . import modeltools as poe2
# Create your tests here.

class SimpleTestCase(TestCase):
    def test_registration(self):
        url = reverse("registration_register")
        response = self.client.post(url, {
            "username":'mike2001',
            "password1":"password123",
            "password2":"password123",
            "poe_sessid": "lkjhkjh23",
            "email": "s@s.com"
        })
        self.assertEqual(response.status_code, 302) 
        models.PoeUser.objects.get(username = "mike2001")
        session = self.client.session
   
    def test_index_page(self):
        url = reverse("index")
        response = self.client.post(url)
        self.assertIn(b'<h1>Rango says... hello!</h1>', response.content)

    def test_registration_login(self):
        url = reverse("registration_register")
        response = self.client.post(url, {
            "username":'mike2001',
            "password1":"password123",
            "password2":"password123",
            "poe_sessid": "lkjhkjh23",
            "email": "s@s.com"
        })
        self.assertEqual(response.status_code, 302) 
        models.PoeUser.objects.get(username = "mike2001")
        session_key = self.client.session.session_key
        ####
        url = reverse('index')
        response = self.client.post(url)


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
        data = models.PrefixTypes.objects.all()
        self.assertEqual(len(data), 33)
        
    def test_length_prefix_names(self):
        #length of prefix names 302
        data = models.PrefixNames.objects.all()
        self.assertEqual(len(data), 302)
   
    def test_length_prefixes(self):
        #length of prefixes 1035
        #length of z once the inner stat dictionary of the higher list is known
        data = models.Prefixes.objects.all()
        self.assertEqual(len(data), 1035)
## Suffixes      
    def test_length_suffix_types(self):
        #length of suffix_types =  24
        data = models.SuffixTypes.objects.all()
        self.assertEqual(len(data), 24)
        
    def test_length_suffix_names(self):
        #length of suffix names 247
        data = models.SuffixNames.objects.all()
        self.assertEqual(len(data), 247)
   
    def test_length_suffixes(self):
        #length of suffixes 420
        #length of z once the inner stat dictionary of the higher list is known
        data = models.Suffixes.objects.all()
        self.assertEqual(len(data), 420)

## weapons
    def test_length_weapon_names(self):
        #length of weapon names 307
        data = models.WeaponNames.objects.all()
        self.assertEqual(len(data), 307)

    def test_length_weapon_stats(self):
        #length of weapon stats 250
        data = models.WeaponStats.objects.all()
        self.assertEqual(len(data), 250)

## clothes
    def test_length_clothes_names(self):
        #length of clothes names 362
        data = models.ClothesNames.objects.all()
        self.assertEqual(len(data), 362)

    def test_length_clothes_stats(self):
        #length of clothesweapon stats 244
        data = models.ClothesStats.objects.all()
        self.assertEqual(len(data), 244)

## jewelry
    def test_length_jewelry_names(self):
        #length of jewelry names 74
        data = models.JewelryNames.objects.all()
        self.assertEqual(len(data), 74)

    def test_length_jewelry_stats(self):
        #length of jewelry stats 111
        data = models.JewelryStats.objects.all()
        self.assertEqual(len(data), 111)

## Stats
    def test_length_stats(self):
        #length of stats  1530
        #length of z once the inner stat dictionary of the higher list is known
        data = models.Stats.objects.all()
        self.assertEqual(len(data), 1530)
        
    def test_length_stat_names(self):
        #length of stat_names 266
        #length of z once the inner stat dictionary of the higher list is known
        data = models.StatNames.objects.all()
        self.assertEqual(len(data), 266)

class GenericDataTablecontents(TestCase):
    print("GenericDataTablecontents")
    multi_db = True
    fixtures = ["poe/fixtures/dumpdata.yaml",]
    
    def test_category_type(self):
        data = models.CategoryTypes.objects.all()
        names = []
        print("category_types", data)
        for x in data:
            names.append(x.name)
        names.sort()
        self.assertListEqual(names, ['Clothes', 'Jewelry', 'Weapons'])

    def test_item_types(self):
        data = models.ItemTypes.objects.all()
        print("item_types", data)
        names = []
        for x in data:
            print ("x.name", x.name)
            names.append(x.name)
        names.sort()
        self.assertListEqual(names, [
            'Amulet', 'Belt', 'Body Armour', 'Boots', 'Bow', 'Claw', 'Dagger', 
            'Gloves', 'Helmet', 'One Hand Axe', 'One Hand Mace', 
            'One Hand Sword', 'Ring', 'Sceptre', 'Shield', 'Staff', 
            'Thrusting One Hand Sword', 'Two Hand Axe', 'Two Hand Mace', 
            'Two Hand Sword', 'Wand'])
        
        
    
    def test_assert_lists(self):
        a = ["dave", "adam", "clive"]
        a.sort()
        self.assertListEqual(a, ["adam", "clive", "dave"])
'''
d = modeltools.get_stat_ids_from_stat_name("Weapon Elemental Damage +%")
stat_list = [int(i[0]) for i in d.values_list("id")]
modeltools.get_suffix_names_from_stat_id(stat_list)'''        
        
