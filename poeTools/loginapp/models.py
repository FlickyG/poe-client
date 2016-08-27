# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Accounts(models.Model):
    id = models.AutoField()
    ggg_account_name = models.CharField(max_length=50)
    gg_sessid = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accounts'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CharTypes(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'char_types'


class Characters(models.Model):
    name = models.CharField(max_length=50)
    account_id = models.IntegerField()
    level = models.IntegerField()
    class_field = models.CharField(db_column='class', max_length=25)  # Field renamed because it was a Python reserved word.
    league = models.CharField(max_length=25)
    classid = models.IntegerField()
    ascendancyclass = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'characters'


class ClothesNames(models.Model):
    name = models.CharField(unique=True, max_length=50)
    c_type = models.CharField(max_length=30, blank=True, null=True)
    i_level = models.SmallIntegerField()
    armour = models.SmallIntegerField()
    evasion = models.SmallIntegerField()
    energy_shield = models.FloatField()
    req_str = models.FloatField()
    req_dex = models.SmallIntegerField()
    req_int = models.SmallIntegerField()
    large_url = models.CharField(max_length=800, blank=True, null=True)
    small_url = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clothes_names'


class ClothesStats(models.Model):
    id = models.AutoField()
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


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class JewelryNames(models.Model):
    j_type = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    i_level = models.SmallIntegerField()
    large_url = models.CharField(max_length=800, blank=True, null=True)
    small_url = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jewelry_names'


class JewelryStats(models.Model):
    id = models.AutoField()
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
    type_id = models.IntegerField()
    name_id = models.IntegerField()
    i_level = models.IntegerField()
    crafted = models.BooleanField()
    stat = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'prefixes'
        unique_together = (('type_id', 'name_id', 'i_level', 'crafted', 'stat'),)


class StatNames(models.Model):
    name = models.CharField(unique=True, max_length=60)

    class Meta:
        managed = False
        db_table = 'stat_names'


class Stats(models.Model):
    name_id = models.IntegerField()
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
    type_id = models.IntegerField()
    name_id = models.IntegerField()
    i_level = models.IntegerField()
    crafted = models.BooleanField()
    stat = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'suffixes'
        unique_together = (('type_id', 'name_id', 'i_level', 'crafted', 'stat'),)


class WeaponNames(models.Model):
    name = models.CharField(unique=True, max_length=50)
    w_type = models.CharField(max_length=30, blank=True, null=True)
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

    class Meta:
        managed = False
        db_table = 'weapon_names'


class WeaponStats(models.Model):
    id = models.AutoField()
    w_id = models.IntegerField()
    s_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'weapon_stats'


class WeaponTypes(models.Model):
    type = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'weapon_types'
