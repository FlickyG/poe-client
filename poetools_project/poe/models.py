from django.db import models
from django.db import utils 
from django.template.defaultfilters import slugify #section 7.3
from django.contrib.auth.models import User #section 9

import autoslug

from django.db.models.signals import post_save #for custom user profile
from django.dispatch import receiver #for custom user profile

from autoslug import AutoSlugField

import logging

stdlogger = logging.getLogger(__name__)
stdlogger.warn("Entering poe.models")

# Create your models here.
class Category(models.Model):
    """
    An artifact from the tango with django tutorial
    """
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        # Uncomment if you don't want the slug to change every time the name changes
        #if self.id is None:
                #self.slug = slugify(self.name)
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
            return str(self.name)

class Page(models.Model):
    """
    An artifact from the tango with django tutorial
    """
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default =0)

    def __unicode__(self):
        return self.title

class PoeUser(User):
    """
    Is the external version of an account with GGG.  It extends the the
    authentication model (and database) by adding the account name so
    that we can delete the psql 'item' db and leave the authentication one 
    intact.  This way users do not need to re-register if we wipe the psql.
    Extends: Django User Model
    Accepts: The account name
    Returns: None, it saves the model
    """
    poe_account_name = models.CharField(max_length = 32)
        
    def __unicode__(self):
        return self.username
    
    class Meta:
        managed = True
        #model_label = "poeuser"

    def save(self, *args, **kwargs):
        super(PoeUser, self).save(*args, **kwargs)
        x = PoeAccount(acc_name = self.poe_account_name)
        x.save()

class ItemCategory(models.Model):
    """
    Represents the highest level of loot categorisation.  E.G. Weapons, Armour
    """
    name = models.CharField(unique = True, max_length = 50)
    slug = models.SlugField()

    class Meta:
        managed = True
        db_table = 'item_category'
        app_label = "poe" 
    
    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        # Uncomment if you don't want the slug to change every time the name changes
        #if self.id is None:
        #self.slug = slugify(self.name)
        self.slug = slugify(self.name)
        super(ItemCategory, self).save(*args, **kwargs)
    
class ItemType(models.Model):
    """
    Represents the type of an item, e.g. Dagger, Ring, Bow
    """    
    name = models.CharField(unique = True, max_length = 50)
    type = models.ForeignKey(ItemCategory)
    slug = models.SlugField()

    class Meta:
        managed = True
        db_table = 'item_type'
        app_label = "poe" 

    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        # Uncomment if you don't want the slug to change every time the name changes
        #if self.id is None:
        #self.slug = slugify(self.name)
        self.slug = slugify(self.name)
        super(ItemType, self).save(*args, **kwargs)

class StatNames(models.Model):
    """
    For explicit item mods, represents the fundamental benefit, e.g. Added Life, + Attributes,
    """
    name = models.CharField(unique=True, max_length=60)
    slug = models.SlugField(max_length = 75)

    class Meta:
        managed = True
        db_table = 'stat_names'
        app_label = "poe"
        
    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        # Uncomment if you don't want the slug to change every time the name changes
        #if self.id is None:
        #self.slug = slugify(self.name)
        self.slug = slugify(self.name)
        super(StatNames, self).save(*args, **kwargs)

class Stats(models.Model):
    """
    Numerates the extent of the fundamental benefit, e.g. +3! to Life
    """
    name = models.ForeignKey(StatNames, models.DO_NOTHING)
    min_value = models.IntegerField()
    max_value = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'stats'
        app_label = "poe"
        unique_together = ('name', 'min_value', 'max_value',)

    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        # Uncomment if you don't want the slug to change every time the name changes
        #if self.id is None:
        #self.slug = slugify(self.name)
        self.slug = slugify(self.name)
        super(Stats, self).save(*args, **kwargs)
        
class FixCategory(models.Model):
    """
    E.G. Prefix or Suffix
    """
    name = models.CharField(unique = True, blank = False, max_length = 50)
    slug = models.SlugField()

    
    class Meta:
        managed = True
        db_table = 'fix_category'
        app_label = "poe"

    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        # Uncomment if you don't want the slug to change every time the name changes
        #if self.id is None:
        #self.slug = slugify(self.name)
        self.slug = slugify(self.name)
        super(FixCategory, self).save(*args, **kwargs)

class FixType(models.Model):
    """
    For prefix or suffixes, represents the fundamental benefit,
    e.g. Added Life, + Attributes,
    """
    name = models.CharField(max_length = 50)
    category = models.ForeignKey(FixCategory)
    slug = models.SlugField()
    
    class Meta:
        managed = True
        db_table = 'fix_type'
        app_label = "poe"

    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        # Uncomment if you don't want the slug to change every time the name changes
        #if self.id is None:
        #self.slug = slugify(self.name)
        self.slug = slugify(self.name)
        super(FixType, self).save(*args, **kwargs)

class FixName(models.Model):
    """
    For explicit item mods, represents the in game name e.g. Infernal, Vicious
    """
    name = models.CharField(max_length=50)
    type = models.ForeignKey(FixType)
    slug = models.SlugField()
    
    class Meta:
        managed = True
        db_table = 'fix_name'
        app_label = "poe"

    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        # Uncomment if you don't want the slug to change every time the name changes
        #if self.id is None:
        #self.slug = slugify(self.name)
        self.slug = slugify(self.name)
        super(FixName, self).save(*args, **kwargs)

class Fix(models.Model):
    """
    For Prefix and Suffixes, links together the fundamental benefit and the
    numerical extent of this buff
    """
    name = models.ForeignKey(FixName)
    stat = models.ForeignKey(Stats)
    i_level = models.IntegerField()
    m_crafted = models.BooleanField()
    
    class Meta:
        managed = True
        db_table = 'fix'
        app_label = "poe"
        unique_together = ('name', 'stat', 'i_level', 'm_crafted')
        
    def __str__(self):
        return str(self.name)
    

####
####


class ItemName(models.Model):
    """
    Represents an in game loot item
    """
    stdlogger.debug("ItemName")
    name = models.CharField(unique=True, max_length=50)
    i_level = models.SmallIntegerField()
    min_dmg = models.SmallIntegerField(blank=True, null=True)
    max_dmg = models.SmallIntegerField(blank=True, null=True)
    aps = models.FloatField(blank=True, null=True)
    dps = models.FloatField(blank=True, null=True)
    req_str = models.SmallIntegerField(blank=True, null=True)
    req_dex = models.SmallIntegerField(blank=True, null=True)
    req_int = models.SmallIntegerField(blank=True, null=True) 
    large_url = models.CharField(max_length=800, blank=True)
    small_url = models.CharField(max_length=400, blank=True)
    armour = models.SmallIntegerField(blank=True, null=True)
    evasion = models.SmallIntegerField(blank=True, null=True)
    energy_shield = models.FloatField(blank=True, null=True)
    type = models.ForeignKey(ItemType)
    stats = models.ManyToManyField(Stats)
    slug = models.SlugField()
    
    class Meta:
        managed = True
        db_table = 'item_name'
        app_label = "poe"
    
    @property
    def len_stats(self):
        names = [x.name.name for x in self.stats.all()]
        l = len(self.stats.all())
        m = ''.join((__name__, " length of stats ", str(l)))
        self.clsslogger.debug(m)
        return len(self.stats.all())
    
    @property
    def stat_names(self):
        names = [x.name.name for x in self.stats.all()]
        try:
            pass
            #stdlogger.debug("Entering index method")
        except Exception:
            print("eeee")    
        self.clsslogger.debug(names)
        return names #len(self.stats.all())
#poe.models.ItemName.objects.filter(name = "Avian Twins Talisman")[0].stat_names[0]
#need to insert colspan in the template but I think we need to know the length of the stats
#and for that we need java script, no other means of calculating this in html

    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        # Uncomment if you don't want the slug to change every time the name changes
        #if self.id is None:
        #self.slug = slugify(self.name)
        self.slug = slugify(self.name)
        super(ItemName, self).save(*args, **kwargs)

class ItemStat(models.Model):
    """
    Links items with their stats.
    """
    i = models.ForeignKey(ItemName, models.DO_NOTHING)
    s = models.ForeignKey(Stats, models.DO_NOTHING)
    
    class Meta:
        managed = True
        db_table = 'item_stat'
        app_label = "poe"
    
    def __str__(self):
        return str(self.i.name)
    
    def save(self, *args, **kwargs):
        # Uncomment if you don't want the slug to change every time the name changes
        #if self.id is None:
        super(ItemStat, self).save(*args, **kwargs)
        
###
### GGG Characters
###
class PoeAccount(models.Model):
    """
    Is the internal version of an account with GGG.  It clumsily mirrors the
    built in authentication model and adds the GGG session id required to access
    the online API.
    We use this approach so that we can delete the psql 'item' db and leave the
    authentication one intact.  This way users do not need to re-register if we
    wipe the psql.
    """
    acc_name = models.CharField(max_length=32, blank=False, )
    sessid = models.CharField(max_length=32, blank=False, )
  
    class Meta:
        managed = True
        db_table = 'poe_account'
        app_label = 'poe'
        
    def __str__(self):
        return str(self.acc_name)

class PoeItem(models.Model):
    """
    Links an in game loot item to it's owner
    >>> pprint.pprint(the_tab_items[2])
    {'corrupted': False,
     'frameType': 0,
     'h': 3,
     'icon': 'https://web.poecdn.com/image/Art/2DItems/Weapons/OneHandWeapons/OneHandSwords/OneHandSword2.png?scale=1&w=1&h=3&v=a94ce74a6007ca561bb3a4bfa3abe15b3',
     'id': '1f2c3ec221bb62af70981c8adb6b29d7984aac5ca1faa5b33cd0393a7961c6cc',
     'identified': True,
     'ilvl': 57,
     'implicitMods': ['+400 to Accuracy Rating'],
     'inventoryId': 'Stash3',
     'league': 'Legacy',
     'lockedToCharacter': False,
     'name': '',
     'properties': [{'displayMode': 0, 'name': 'One Handed Sword', 'values': []},
                    {'displayMode': 0,
                     'name': 'Quality',
                     'type': 6,
                     'values': [['+14%', 1]]},
                    {'displayMode': 0,
                     'name': 'Physical Damage',
                     'type': 9,
                     'values': [['44-95', 1]]},
                    {'displayMode': 0,
                     'name': 'Critical Strike Chance',
                     'type': 12,
                     'values': [['5.00%', 0]]},
                    {'displayMode': 0,
                     'name': 'Attacks per Second',
                     'type': 13,
                     'values': [['1.30', 0]]},
                    {'displayMode': 0,
                     'name': 'Weapon Range',
                     'type': 14,
                     'values': [['9', 0]]}],
     'requirements': [{'displayMode': 0, 'name': 'Level', 'values': [['56', 0]]},
                      {'displayMode': 1, 'name': 'Str', 'values': [['96', 0]]},
                      {'displayMode': 1, 'name': 'Dex', 'values': [['96', 0]]}],
     'socketedItems': [],
     'sockets': [{'attr': 'S', 'group': 0}],
     'typeLine': 'Superior Gemstone Sword',
     'verified': False,
     'w': 1,
     'x': 10,
     'y': 1} 
    """
    name = models.CharField(max_length = 264, blank = False, )
    owner = models.ForeignKey(PoeAccount) 
    ggg_id = models.CharField(max_length = 100, blank = True, )
    raw_data = models.CharField(max_length = 2048, blank = True, )
    ilvl = models.IntegerField()
    tab_location = models.IntegerField()
    x_location = models.IntegerField()
    y_location = models.IntegerField()
    req_lvl = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    req_str = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    req_int = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    req_dex = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    
    @property
    def location(self):
        return (self.tab_location,
                self.x_location,
                self.y_location,)
    

class PoeCharacter(models.Model):
    """
    Represents the high level data of a PoE Character
    """
    account = models.ForeignKey(PoeAccount) 
    name = models.CharField(max_length = 64, null=True)
    eg = {
         'level': 70,
         'class': 'Duelist',
         'ascendancyClass': 0,
         'classId': 4,
         'league': 'Standard',
         'name': 'Flicky_Dagger'
         }
    level = models.IntegerField()
    ggg_class = models.CharField(max_length = 32)
    ascendancy_class = models.IntegerField()
    classId = models.CharField(max_length = 64)
    league = models.CharField(max_length = 64)
    # Equipped Weapons
    Weapon = models.OneToOneField(PoeItem,
                                  null = True,
                                  related_name = '%(class)s_weapon'
                                  )
   
    Offhand = models.OneToOneField(PoeItem,
                                   related_name = '%(class)s_offhand',
                                   null = True,
                                   )
    
    Weapon2 = models.OneToOneField(PoeItem,
                                   null = True,
                                   related_name = "%(class)s_weapon2",
                                   )
    Offhand2 = models.OneToOneField(PoeItem,
                                   null = True,
                                   related_name = "%(class)s_offhand2",
                                   )
    # Equipped Armour
    Helm = models.OneToOneField(PoeItem,
                                   null = True,
                                   related_name = "%(class)s_helm",
                                   )
    BodyArmour = models.OneToOneField(PoeItem,
                                   null = True,
                                   related_name = "%(class)s_bodyarmour",
                                   )
    Gloves = models.OneToOneField(PoeItem,
                                   null = True,
                                   related_name = "%(class)s_gloves",
                                   )
    Belt = models.OneToOneField(PoeItem,
                                   null = True,
                                   related_name = "%(class)s_belt",
                                   )
    Boots = models.OneToOneField(PoeItem,
                                   null = True,
                                   related_name = "%(class)s_boots",
                                   )
    # Equipped Jewelry
    Amulet = models.OneToOneField(PoeItem,
                                   null = True,
                                   related_name = "%(class)s_amulet",
                                   )
    Ring = models.OneToOneField(PoeItem,
                                   null = True,
                                   related_name = "%(class)s_ring",
                                   )
    Ring2 = models.OneToOneField(PoeItem,
                                   null = True,
                                   related_name = "%(class)s_ring2",
                                   )
    MainInventory = models.OneToOneField(PoeItem,
                                   null = True,
                                   related_name = "%(class)s_maininventory",
                                   )
    Flask = models.OneToOneField(PoeItem,
                                   null = True,
                                   related_name = "%(class)s_flask",
                                   )

class PoeTab(models.Model):
    """
    Represents the info surrounding each stash tab in-game
    """
    index = models.IntegerField()
    ggg_identifier = models.CharField(max_length = 64)
    name = models.CharField(max_length = 64, blank = True)
    owner = models.ForeignKey(PoeAccount)
    """
    >>> pprint.pprint(the_tabs[0])
    {'colour': {'b': 0, 'g': 128, 'r': 99},
     'hidden': False,
     'i': 0,
     'id': 'fd12b8d1efe0bc34fb8f84e8438d3ae16cd6b923b0e87c67dbea96d6871d2267',
     'n': '$',
     'selected': True,
     'srcC': 'https://web.poecdn.com/gen/image/YTozOntpOjA7aToyNDtp/OjE7czozMjoiMDJhMTk3/N2QxZDAzNDQzNmU3NzM5/ZjgzZDEzYjIwN2YiO2k6/MjthOjI6e2k6MDtpOjI7/aToxO2E6Mzp7czoxOiJ0/IjtpOjI7czoxOiJuIjtz/OjA6IiI7czoxOiJjIjtp/Oi0xMDI1NjM4NDt9fX0,/d6161fcf22/Stash_TabC.png',
     'srcL': 'https://web.poecdn.com/gen/image/YTozOntpOjA7aToyNDtp/OjE7czozMjoiMDJhMTk3/N2QxZDAzNDQzNmU3NzM5/ZjgzZDEzYjIwN2YiO2k6/MjthOjI6e2k6MDtpOjI7/aToxO2E6Mzp7czoxOiJ0/IjtpOjE7czoxOiJuIjtz/OjA6IiI7czoxOiJjIjtp/Oi0xMDI1NjM4NDt9fX0,/c64747b68d/Stash_TabL.png',
     'srcR': 'https://web.poecdn.com/gen/image/YTozOntpOjA7aToyNDtp/OjE7czozMjoiMDJhMTk3/N2QxZDAzNDQzNmU3NzM5/ZjgzZDEzYjIwN2YiO2k6/MjthOjI6e2k6MDtpOjI7/aToxO2E6Mzp7czoxOiJ0/IjtpOjM7czoxOiJuIjtz/OjA6IiI7czoxOiJjIjtp/Oi0xMDI1NjM4NDt9fX0,/1185e76da6/Stash_TabR.png',
     'type': 'CurrencyStash'}    
    """
    class Meta: 
        managed = True
        db_table = 'poe_tab'
        app_label = 'poe'
        
    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        # Uncomment if you don't want the slug to change every time the name changes
        #if self.id is None:
                #self.slug = slugify(self.name)
        self.name = slugify(self.name)
        super(PoeTab, self).save(*args, **kwargs)


    
    
