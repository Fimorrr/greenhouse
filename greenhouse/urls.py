"""greenhouse URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from app import views

urlpatterns = [
    url(r'^$', views.water),
    url(r'^help/$', views.help),
    url(r'^about/$', views.about),
    url(r'^comp/$', views.comp),
    url(r'^sev/$', views.sev),
    url(r'^monitor/$', views.water),
    url(r'^entry/(?P<id>\d+)/$', views.phase_entry),
    url(r'^entry/add/(?P<group>\d+)/$', views.entry_add),
    url(r'^entry/edit/(?P<group>\d+)/(?P<id>\d+)/$', views.entry_edit),
    url(r'^entry/delete/(?P<group>\d+)/(?P<id>\d+)/$', views.entry_delete),
    url(r'^book/$', views.plant),
    url(r'^book/plant/$', views.plant),
    url(r'^group/$', views.group),
    url(r'^group/add/$', views.group_add),
    url(r'^group/edit/(?P<id>\d+)/$', views.group_edit),
    url(r'^group/delete/(?P<id>\d+)/$', views.group_delete),
    url(r'^plant/add/$', views.plant_add),
    url(r'^plant/edit/(?P<id>\d+)/$', views.plant_edit),
    url(r'^plant/delete/(?P<id>\d+)/$', views.plant_delete),
    url(r'^book/phase/$', views.phase),
    url(r'^phase/add/$', views.phase_add),
    url(r'^phase/edit/(?P<id>\d+)/$', views.phase_edit),
    url(r'^phase/delete/(?P<id>\d+)/$', views.phase_delete),
    url(r'^room/$', views.room),
    url(r'^room/add/$', views.room_add),
    url(r'^room/edit/(?P<id>\d+)/$', views.room_edit),
    url(r'^room/delete/(?P<id>\d+)/$', views.room_delete),
    url(r'^monitor/water/$', views.water),
    url(r'^monitor/light/$', views.light),
    url(r'^monitor/heat/$', views.heat),
    url(r'^monitor/cold/$', views.cold),
    url(r'^admin/', admin.site.urls),
]
