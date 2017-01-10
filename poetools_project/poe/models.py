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
        print("slugField = ", models.SlugField)
        slug = models.SlugField()

        def save(self, *args, **kwargs):
                # Uncomment if you don't want the slug to change every time the name changes
                #if self.id is None:
                        #self.slug = slugify(self.name)
                self.slug = slugify(self.name)
                super(Category, self).save(*args, **kwargs)

        def __unicode__(self):
                return self.name

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
    
class ClothesNames(models.Model):
    name = models.CharField(unique=True, max_length=50)
    i_level = models.SmallIntegerField()
    armour = models.SmallIntegerField()
    evasion = models.SmallIntegerField()
    energy_shield = models.FloatField()
    req_str = models.FloatField()
    req_dex = models.SmallIntegerField()
    req_int = models.SmallIntegerField()
    large_url = models.CharField(max_length=800, blank=True, null=True)
    small_url = models.CharField(max_length=400, blank=True, null=True)
    c_type = models.ForeignKey('ClothingTypes', models.DO_NOTHING, db_column='c_type', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clothes_names'


class ClothesStats(models.Model):
    c_id = models.SmallIntegerField()
    s_id = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'clothes_stats'


class ClothingTypes(models.Model):
    type = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'clothing_types'
# Unable to inspect table 'django_admin_log'
# The error was: permission denied for relation django_admin_log

# Unable to inspect table 'django_content_type'
# The error was: permission denied for relation django_content_type

# Unable to inspect table 'django_migrations'
# The error was: permission denied for relation django_migrations

# Unable to inspect table 'django_session'
# The error was: permission denied for relation django_session



class JewelryNames(models.Model):
    name = models.CharField(max_length=50)
    i_level = models.SmallIntegerField()
    large_url = models.CharField(max_length=800, blank=True, null=True)
    small_url = models.CharField(max_length=400, blank=True, null=True)
    j_type = models.ForeignKey('JewelryTypes', models.DO_NOTHING, db_column='j_type', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jewelry_names'


class JewelryStats(models.Model):
    j_id = models.SmallIntegerField()
    s_id = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'jewelry_stats'


class JewelryTypes(models.Model):
    type = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'jewelry_types'
# Unable to inspect table 'loginapp_userprofile'
# The error was: permission denied for relation loginapp_userprofile



class PrefixNames(models.Model):
    name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'prefix_names'


class PrefixTypes(models.Model):
    type = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'prefix_types'


class Prefixes(models.Model):
    type = models.ForeignKey(PrefixTypes, models.DO_NOTHING)
    name = models.ForeignKey(PrefixNames, models.DO_NOTHING)
    i_level = models.IntegerField()
    crafted = models.BooleanField()
    stat = models.ForeignKey('Stats', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'prefixes'
        unique_together = (('type', 'name', 'i_level', 'crafted', 'stat'),)


class StatNames(models.Model):
    name = models.CharField(unique=True, max_length=60)

    class Meta:
        managed = False
        db_table = 'stat_names'


class Stats(models.Model):
    name = models.ForeignKey(StatNames, models.DO_NOTHING)
    min_value = models.IntegerField()
    max_value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stats'


class SuffixNames(models.Model):
    name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'suffix_names'


class SuffixTypes(models.Model):
    type = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'suffix_types'


class Suffixes(models.Model):
    type = models.ForeignKey(SuffixTypes, models.DO_NOTHING)
    name = models.ForeignKey(SuffixNames, models.DO_NOTHING)
    i_level = models.IntegerField()
    crafted = models.BooleanField()
    stat = models.ForeignKey(Stats, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'suffixes'
        unique_together = (('type', 'name', 'i_level', 'crafted', 'stat'),)


class WeaponNames(models.Model):
    name = models.CharField(unique=True, max_length=50)
    i_level = models.SmallIntegerField()
    min_dmg = models.SmallIntegerField()
    max_dmg = models.SmallIntegerField()
    aps = models.FloatField()
    dps = models.FloatField()
    req_str = models.SmallIntegerField()
    req_dex = models.SmallIntegerField()
    req_int = models.SmallIntegerField()
    large_url = models.CharField(max_length=800, blank=True, null=True)
    small_url = models.CharField(max_length=400, blank=True, null=True)
    w_type = models.ForeignKey('WeaponTypes', models.DO_NOTHING, db_column='w_type', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weapon_names'


class WeaponStats(models.Model):
    w = models.ForeignKey(WeaponNames, models.DO_NOTHING)
    s = models.ForeignKey(Stats, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'weapon_stats'


class WeaponTypes(models.Model):
    type = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'weapon_types'