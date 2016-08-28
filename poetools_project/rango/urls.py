from django.conf.urls import url
from rango import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^hello$', views.hello_world, name = 'hello'),
        url(r'^about', views.about, name = 'about')
        ]