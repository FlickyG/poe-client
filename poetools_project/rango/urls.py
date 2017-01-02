from django.conf.urls import url
from rango import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'), # end of section 8
    url(r'^add_category/$', views.add_category, name='add_category'), # NEW MAPPING!
    url(r'^add_page/$', views.add_page, name='add_page'), # NEW MAPPING!
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),  # section 7.3,
    url(r'^register/$', views.register, name='register'), # section 9
    url(r'^login/$', views.user_login, name='login'), # section 9
    url(r'^restricted/', views.restricted, name='restricted'), #sectio9 9
    url(r'^logout/$', views.user_logout, name='logout'),
        ]