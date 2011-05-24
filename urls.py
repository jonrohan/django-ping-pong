from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
    url(r'^pingpong/$', pingpong, name="pingpong"),
    url(r'^pingpong/(?P<match_id>[0-9]+)/$', match, name="pingpong_match"),
    url(r'^pingpong/new/$', new_match, name="new_pingpong"),
)
