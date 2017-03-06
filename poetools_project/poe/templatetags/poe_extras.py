from django import template
from poe.models import ItemCategory, FixCategory

register = template.Library()

@register.inclusion_tag('poe/cats.html')
def get_item_category_list():
    return {'item_cats': ItemCategory.objects.all()}

@register.inclusion_tag('poe/fixes.html')
def get_fix_category_list():
    return {'fix_cats': FixCategory.objects.all()}


