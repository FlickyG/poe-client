from django.conf.urls import url
from poe import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^item/(?P<category_name_slug>[\w\-]+)/$', views.item, name='item'), # end of section 8
    url(r'^item/(?P<category_name_slug>[\w\-]+)/(?P<sub_category_slug>[\w\-]+)/$', views.item, name='item'), # end of section 8
    url(r'^mods/(?P<category_name_slug>[\w\-]+)/$', views.mods, name='mods'), # end of section 8
    url(r'^restricted/', views.restricted, name='restricted'), #sectio9 9
    url(r'characters/(?P<account_name_slug>[\w\-]+)/$', views.ggg_characters, name = 'ggg_characters'),
    url(r'download_ggg_data/(?P<account_name_slug>[\w\-]+)/$', views.get_data, name = "download_ggg_data"),
    ]