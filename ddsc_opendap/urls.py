# (c) Nelen & Schuurmans.  MIT licensed, see LICENSE.rst.
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from lizard_ui.urls import debugmode_urlpatterns

from ddsc_opendap import views

urlpatterns = patterns(
    '',
    )
urlpatterns += debugmode_urlpatterns()
