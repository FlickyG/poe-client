from django.shortcuts import render

from poe.models import Category #sectio9n 7.1

from poe.models import Page #section 7.3

from poe.forms import CategoryForm #section 8

#from poe.forms import UserForm, UserProfileForm #sectio9n 9
from django.contrib.auth import authenticate, login #sectio9n 9
from django.http import HttpResponseRedirect, HttpResponse #sectio9n 9
from django.contrib.auth.decorators import login_required #section 9
from django.contrib.auth import logout #section 9

# Create your views here.
from django.http import HttpResponse
import datetime
#from datetime import datetime

from poe.forms import PageForm

def index(request):

    request.session.set_test_cookie()
    
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}

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

#section 7.3
def category(request, category_name_slug):

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


