from django.shortcuts import render

from poe.models import FixCategory, Fix

from poe.models import Category, Page #section 7.3

from poe.models import ItemCategory
from poe.models import FixCategory
from poe.models import FixType
from poe.models import ItemType
from poe.models import ItemName

from poe.forms import CategoryForm #section 8

import poe.common.character_tools

#from poe.forms import UserForm, UserProfileForm #sectio9n 9
from django.contrib.auth import authenticate, login #sectio9n 9
from django.http import HttpResponseRedirect, HttpResponse #sectio9n 9
from django.contrib.auth.decorators import login_required #section 9
from django.contrib.auth import logout #section 9

# Create your views here.
from django.http import HttpResponse
import datetime
import sys


from poe.forms import PageForm
import poe.tables
from django_tables2.config import RequestConfig


def index(request):

    request.session.set_test_cookie()
    item_category_list = ItemCategory.objects.all()
    modifications_list = FixCategory.objects.all()

    context_dict = {'item_categories': item_category_list, 'mods': modifications_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits


    response = render(request,'poe/index.html', context_dict)

    return response

def index_rango(request):

    request.session.set_test_cookie()
    
    # fetch items
    # fetch categories
    category_list = FixCategory.objects.all()
    print("hello index view", category_list)
    context_dict = {'categories': category_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits


    response = render(request,'poe/index.html', context_dict)

    return response


def about(request):
    
    context_dict = {'helloimage': 'download.png', 'boldmessage': datetime.datetime.now()}
    
    # If the visits session varible exists, take it and use it.
    # If it doesn't, we haven't visited the site so set the count to zero.
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0
    context_dict['visits'] = count
    context_dict['last_visit'] = request.session.get('last_visit')
    # remember to include the visit data
    return render(request, 'poe/about.html', context_dict)


def hello_world(request):
    return HttpResponse("Adam says hello world!")

def item(request, category_name_slug, sub_category_slug = None):
    print("category_name_slug, sub_category_slug", category_name_slug, sub_category_slug)

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        item_category = ItemCategory.objects.get(slug = category_name_slug)
        context_dict['item_name'] = item_category.name
        # Retrieve all of the associated item categories e.g. all the weapon type.
        # Add the results 
        context_dict['items'] = ItemType.objects.filter(type_id=item_category.id)
        #context_dict['table'] = poe.tables.ItemTable(ItemType.objects.filter(type_id=item_category.id))
        # We also add the category object from the database to the context
        # dictionary We'll use this in the template to verify that the category exists.
        context_dict['category'] = item_category
        # add the category slug so we can use it recursively when clicking 
        # through the webpage
        context_dict['slug'] = category_name_slug
        if sub_category_slug != None:  # if the sub category is present 
            # select sub category
            try:
                #pass
                # select sub category objects
                sub_item_category = ItemType.objects.get(slug = sub_category_slug)
                context_dict['sub_item_category'] = sub_item_category
                context_dict['sub_item_name'] = sub_item_category.name
                context_dict['sub_items'] = ItemName.objects.filter(type_id=sub_item_category.id)
                if item_category.name == "Weapons":
                    table = poe.tables.WeaponTable(ItemName.objects.filter(type_id=sub_item_category.id))   
                elif item_category.name == 'Clothes':
                    table = poe.tables.ClothingTable(ItemName.objects.filter(type_id=sub_item_category.id))
                elif item_category.name == 'Jewelry':
                    table = poe.tables.JewelTable(ItemName.objects.filter(type_id=sub_item_category.id))
                else:
                    print("something went wrong", item_category)
                    sys.exit()
                RequestConfig(request).configure(table)
                context_dict['table'] = table
            except:
                pass
        else:
            pass # ignore if None
    except ItemType.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        print("something went wrong with poe.views.item")
        pass

    # Go render the response and return it to the client.
    return render(request, 'poe/item.html', context_dict)

def mods(request, category_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        item_category = FixCategory.objects.get(slug=category_name_slug)
        context_dict['mod_name'] = item_category.name

        # Retrieve all of the associated item categories e.g. all the weapon type.
        # Note that filter returns >= 1 model instance.
        mods = FixType.objects.filter(category_id=item_category.id)
        # Adds our results list to the template context under name pages.
        context_dict['mods'] = mods

        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = item_category
        #section 8
        context_dict['slug'] = category_name_slug
    except ItemType.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        print("something went wrong with poe.views.item")
        pass

    # Go render the response and return it to the client.
    return render(request, 'poe/mods.html', context_dict)

#section 7.3
def category_rango(request, category_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
        #section 8
        context_dict['slug'] = category_name_slug
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'poe/category.html', context_dict)

#section 8
def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'poe/add_category.html', {'form': form})



def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            print("form is valid")
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print("form has errors")
            print(form.errors)
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat,'category_name_slug': category_name_slug}

    return render(request, 'poe/add_page.html', context_dict)



@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def ggg_characters(request):
    print("hello world from gg_characters")
    poe.common.character_tools.get_characters(user)
    return render(request, 'poe/ggg_characters.html')
