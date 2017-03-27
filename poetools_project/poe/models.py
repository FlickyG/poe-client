from django.db import models
from django.db import utils 
from django.template.defaultfilters import slugify #section 7.3
from django.contrib.auth.models import User #section 9

import autoslug

from django.db.models.signals import post_save #for custom user profile
from django.dispatch import receiver #for custom user profile

from autoslug import AutoSlugField

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
    stats = models.ManyToManyField(Stats)
    slug = models.SlugField()
    
    class Meta:
        managed = True
        db_table = 'item_name'
        app_label = "poe"
    
    @property
    def len_stats(self):
        names = [x.name.name for x in self.stats.all()]
        print("names", names)
        return names #len(self.stats.all())
    
    @property
    def stat_names(self):
        names = [x.name.name for x in self.stats.all()]
        print("names", names)
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
