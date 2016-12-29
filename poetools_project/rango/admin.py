from django.contrib import admin
from rango.models import Category, Page #sectio9n 7.3

# Add in this class to customized the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Register your models here.
from django.contrib import admin
from rango.models import Category, Page

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page)

