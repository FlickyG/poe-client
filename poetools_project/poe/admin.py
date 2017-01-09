from django.contrib import admin
from poe.models import Category, Page #sectio9n 7.3
from poe.models import PoeUser #section 9

# Add in this class to customized the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Register your models here.
from django.contrib import admin
from poe.models import Category, Page, PoeUser



admin.site.register(Category, CategoryAdmin)
admin.site.register(Page)
admin.site.register(PoeUser) 

 
