"""poetools_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings # New Import
from django.conf.urls.static import static # New Import
#from django.conf.urls.defaults import patterns
from django.views.static import serve #to add media url for debug mode
from registration.backends.simple.views import RegistrationView # section 12
from poe.forms import PoeRegistrationForm

admin.autodiscover() #tutorial section 5
#rango
# Create a new class that redirects the user to the index page, if successful at logging
# sectoin 12
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/poe'


urlpatterns = [
    #url(r'^$', include('rango.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^poe/', include('poe.urls')),
    #url(r'^rango/', include('rango.urls')),
    url(r'^accounts/register/$', MyRegistrationView.as_view(form_class=PoeRegistrationForm), name='registration_register'), #section 12, imported urls need to be before default ones
    url(r'^accounts/', include('registration.backends.simple.urls')),
]

# UNDERNEATH your urlpatterns definition, add the following two lines:
if settings.DEBUG:
    urlpatterns.append(
        url(r'^media/(?P<path>.*)$', serve,  {'document_root': settings.MEDIA_ROOT}),
        )
    '''
        url((r'^media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT})),
        ]
        )
    '''
