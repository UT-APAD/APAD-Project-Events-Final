"""The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from django.conf.urls import include, url

urlpatterns = [
    url(r'^fullprice_sub', views.full_price, name='full_price'),
    url(r'^discounted_sub', views.discounted, name='discounted'),
    url(r'^free_sub', views.free, name='free'),
    url(r'^discounted_events', views.discounted_page, name='discounted_page'),
    url(r'^free_events', views.free_page, name='free_page'),
    url(r'^fullprice_events', views.fullprice_page, name='fullprice_page'),
    url(r'^submit_event', views.create, name='create'),
    url(r'^events', views.postSign, name='postSign'),
    url(r'^submitted_event', views.post_create, name='post_create'),
    url(r'^welcome', views.postsignup, name='postsignup'),
    url(r'^$', views.signIn, name='signIn'),
    url(r'^signup', views.signUp,name='signup'),
    url(r'^signin', views.signIn, name='signin'),
    url(r'^my_events', views.my_events, name='my_events'),
    url(r'^specific_event', views.specific_event, name='specific_event'),
    url(r'^contact', views.contact, name='contact')
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()