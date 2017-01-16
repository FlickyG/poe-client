from django.conf.urls import url
from poe import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'), # end of section 8
    url(r'^add_category/$', views.add_category, name='add_category'), # NEW MAPPING!
    url(r'^add_page/$', views.add_page, name='add_page'), # NEW MAPPING!
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),  # section 7.3,
    url(r'^restricted/', views.restricted, name='restricted'), #sectio9 9
        ]