"""qtour URL Configuration

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

from core.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', register),
    url(r'^login/$', qlogin),
    url(r'^$', main),
    url(r'^create_tournament/$', create_tournament),
    url(r'^your_tournaments/$', your_tournaments),
    url(r'^upcoming_tournaments/$', upcoming_tournaments),
    url(r'^past_tournaments/$', past_tournaments),
    url(r'^edit_tournament/(?P<tour_id>[\d]+)/$', edit_tournament),
    url(r'^add_site/(?P<tour_id>[\d]+)/$', add_site),
    url(r'^edit_site/(?P<site_id>[\d]+)/$', edit_site)
]
