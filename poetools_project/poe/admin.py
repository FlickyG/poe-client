from django.contrib import admin
from poe.models import Category, Page #sectio9n 7.3
from poe.models import PoeUser #section 9

from poe.models import ItemCategory
from poe.models import ItemType
from poe.models import ItemName
from poe.models import ItemStat
from poe.models import StatNames
from poe.models import Stats
from poe.models import FixCategory
from poe.models import FixType
from poe.models import FixName
from poe.models import Fix

# Add in this class to customized the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Register your models here.
from django.contrib import admin
from poe.models import Category, Page, PoeUser



admin.site.register(Category, CategoryAdmin)
admin.site.register(Page)
admin.site.register(PoeUser)

admin.site.register(ItemCategory)
admin.site.register(ItemType)
admin.site.register(ItemName)
admin.site.register(ItemStat)
admin.site.register(StatNames)
admin.site.register(Stats)
admin.site.register(FixCategory)
admin.site.register(FixType)
admin.site.register(FixName)
admin.site.register(Fix)


 
from poe.models import ItemCategory
from poe.models import ItemType
from poe.models import ItemName
from poe.models import ItemStat
from poe.models import StatNames
from poe.models import Stats
from poe.models import FixCategory
from poe.models import FixType
from poe.models import FixName
from poe.models import Fix
