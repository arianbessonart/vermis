from django.conf.urls import patterns, url

from invoices import views

urlpatterns = patterns('',
  url(r'^$', 'invoices.views.index', name='index'),
  url(r'^(?P<id>\d+)/$', 'invoices.views.detail', name='detail'),
  url(r'^edit/(?P<id>\d+)/$', 'invoices.views.edit', name='edit'),
  url(r'^create/$', 'invoices.views.create', name='create'),
  url(r'^(?P<id>\d+)/set_charged_invoice/$', 'invoices.views.set_charged_invoice', name='set_charged_invoice'),
  url(r'^generate_pdf/(?P<id>\d+)/$', 'invoices.views.generate_pdf', name='generate_pdf'),
)
