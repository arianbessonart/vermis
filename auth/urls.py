from django.conf.urls import patterns, url

from auth import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'login', views.auth_view),
    url(r'logout', views.logout),
)