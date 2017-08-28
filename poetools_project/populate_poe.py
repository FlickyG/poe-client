import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poetools_project.settings')

import django
django.setup()

import poe.models

from poe.models import Category, Page
from poe.models import PoeUser, PoeAccount

def populate():
    python_cat = add_cat('Python')

    add_page(cat=python_cat,
        title="Official Python Tutorial",
        url="http://docs.python.org/2/tutorial/")


    # Print out what we have added to the user.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c

def pop_flicky():
    pass
    for poe_users in poe.models.PoeUser.objects.all():
        # poe_users greenmasterflick flickyg
        print("poe_users", poe_users.poe_account_name, poe_users)
    for poe_account in poe.models.PoeAccount.objects.all():
        print("poe_account", poe_account, poe_account)
    for poe_users in poe.models.PoeUser.objects.all():
        # poe_users greenmasterflick flickyg
        p = PoeAccount.objects.get_or_create(
                acc_name = poe_users.poe_account_name,
                sessid = 'None Saved')[0]
        p.save()
    return p

# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    pop_flicky()