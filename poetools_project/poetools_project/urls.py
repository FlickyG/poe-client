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
admin.autodiscover() #tutorial section 5

urlpatterns = [
    url(r'^$', include('rango.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rango/', include('rango.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# UNDERNEATH your urlpatterns definition, add the following two lines:
if settings.DEBUG:
    print("DEBUG IS SET TRUE", settings.MEDIA_URL)
    urlpatterns.append(
        url(r'^media/(?P<path>.*)$', serve,  {'document_root': settings.MEDIA_ROOT}),
        )
    '''
        url((r'^media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT})),
        ]
        )
    '''
