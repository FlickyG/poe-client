from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse 
from . import models
from . import modeltools
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
        
class GenericDataTestCase(TestCase):
    def test_suffix_names(self):
        d = modeltools.get_stat_ids_from_stat_name("Weapon Elemental Damage +%")
        stat_list = [int(i[0]) for i in d.values_list("id")]
        modeltools.get_suffix_names_from_stat_id(stat_list)        
        
