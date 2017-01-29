from django.db import models
from django.db import utils 
from django.template.defaultfilters import slugify #section 7.3
from django.contrib.auth.models import User #section 9

from django.db.models.signals import post_save #for custom user profile
from django.dispatch import receiver #for custom user profile

# Create your models here.
class Category(models.Model):
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
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default =0)

    def __unicode__(self):
        return self.title

class PoeUser(User):
    poe_sessid = models.CharField(max_length = 32, primary_key = True)
        
    def __unicode__(self):
        return self.username
    
    class Meta:
        managed = True
        #app_label = "poe_auth"

class ItemCategory(models.Model):
    name = models.CharField(unique = True, max_length = 50)

    class Meta:
        managed = True
        db_table = 'item_category'
        app_label = "poe" 
    
    def __str__(self):
        return str(self.name)
    
class ItemType(models.Model):
    name = models.CharField(unique = True, max_length = 50)
    type = models.ForeignKey(ItemCategory)

    class Meta:
        managed = True
        db_table = 'item_type'
        app_label = "poe" 

    def __str__(self):
        return str(self.name)

class StatNames(models.Model):
    name = models.CharField(unique=True, max_length=60)

    class Meta:
        managed = True
        db_table = 'stat_names'
        app_label = "poe"
        
    def __str__(self):
        return str(self.name)

class Stats(models.Model):
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
        
class FixCategory(models.Model):
    name = models.CharField(unique = True, blank = False, max_length = 50)
    
    class Meta:
        managed = True
        db_table = 'fix_category'
        app_label = "poe"

    def __str__(self):
        return str(self.name)

class FixType(models.Model):
    name = models.CharField(max_length = 50)
    category = models.ForeignKey(FixCategory)
    
    class Meta:
        managed = True
        db_table = 'fix_type'
        app_label = "poe"

    def __str__(self):
        return str(self.name)

class FixName(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(FixType)
    
    class Meta:
        managed = True
        db_table = 'fix_name'
        app_label = "poe"

    def __str__(self):
        return str(self.name)

class Fix(models.Model):
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
    
    class Meta:
        managed = True
        db_table = 'item_name'
        app_label = "poe"

    def __str__(self):
        return str(self.name)

class ItemStat(models.Model):
    i = models.ForeignKey(ItemName, models.DO_NOTHING)
    s = models.ForeignKey(Stats, models.DO_NOTHING)
    
    class Meta:
        managed = True
        db_table = 'item_stat'
        app_label = "poe"
