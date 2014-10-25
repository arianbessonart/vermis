from django.conf.urls import patterns, url

from invoices import views

urlpatterns = patterns('',
    url(r'^$', 'invoices.views.index', name='index'),
    url(r'^(?P<id>\d+)/$', 'invoices.views.detail', name='detail'),
    url(r'^edit/(?P<id>\d+)/$', 'invoices.views.edit', name='edit'),
    url(r'^create/$', 'invoices.views.create', name='create'),
)