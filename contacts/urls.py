from django.conf.urls import patterns, url

from contacts import views

urlpatterns = patterns('',
	url(r'^$', 'contacts.views.index', name='index'),
	url(r'^create/$', 'contacts.views.create', name='create'),
	url(r'^edit/(?P<id>\d+)/$', 'contacts.views.edit', name='edit'),
)