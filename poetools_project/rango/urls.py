from django.conf.urls import url
from rango import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^hello$', views.hello_world, name = 'hello'),
        url(r'^about', views.about, name = 'about'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category')  # section 7.3
        ]