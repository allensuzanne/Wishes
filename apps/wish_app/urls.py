from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^wishes$', views.wishes),
    url(r'^wishes/edit/(?P<wish_id>\d+)$', views.wishes_edit_id),
    url(r'^wishes/change/(?P<wish_id>\d+)$', views.wishes_change_id),
    url(r'^wishes/new$', views.wishes_new),
    url(r'^wishes/submit$', views.wishes_submit),
    url(r'^wishes/stats$', views.wishes_stats),
    url(r'^remove/(?P<wish_id>\d+)$', views.remove_id),
    url(r'^granted/(?P<wish_id>\d+)$', views.granted_id),
    url(r'^like/(?P<wish_id>\d+)$', views.like_id),
]
