from django.conf.urls import patterns, url

from clients import views

urlpatterns = patterns('',
	url(r'^$', 'clients.views.index', name='index'),
	url(r'^(?P<id>\d+)/$', 'clients.views.detail', name='detail'),
	url(r'^edit/(?P<id>\d+)/$', 'clients.views.edit', name='edit'),
	url(r'^create/$', 'clients.views.create', name='create'),
)