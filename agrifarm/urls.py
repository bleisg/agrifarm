"""agrifarm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'agrifarm.views.home', name='home'),
    # url(r'^agrifarm/', include('agrifarm.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^bollette/(\d+)/$', 'vendemmia.views.detail', name='detail'),
    url(r'^bollette/$', 'vendemmia.views.index', name='index'),
    url(r'^grafici/$', 'vendemmia.views.grafici', name='grafici'),
    url(r'^grafici_prov/$', 'vendemmia.views.grafici_prov', name='grafici_prov'),
    url(r'^grafici_prov/(\d+)/$', 'vendemmia.views.grafici_singoli', name='grafici_singoli'),
)
