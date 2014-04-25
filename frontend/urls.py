from django.conf.urls import patterns, url

from frontend.views import *


urlpatterns = patterns('frontend.views',
    url(r'^$', GameView.as_view(), name="game"),
)
