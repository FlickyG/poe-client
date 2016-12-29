from django.contrib import admin
from rango.models import Category, Page #sectio9n 7.3
from rango.models import UserProfile #section 9

# Add in this class to customized the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Register your models here.
from django.contrib import admin
from rango.models import Category, Page

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page)
admin.site.register(UserProfile) #section 9
