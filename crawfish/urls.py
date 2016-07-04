"""crawfish URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from crawfish import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('users.urls')),
    url(r'^index/$', views.index, name='index'),
    url(r'^set_level/$', views.set_level),
    url(r'^set_word_limit/$', views.set_word_limit),
    url(r'^bdc/$', views.bdc),
    url(r'^get_sentence', views.get_sentence),
    url(r'^finished_today/$', views.finished_today),
    url(r'^add_note$', views.add_note),
    url(r'^delete_note$', views.delete_note),
]
