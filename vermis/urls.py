from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vermis.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('auth.urls', namespace='auth')),
    url(r'^contacts/', include('contacts.urls', namespace='contacts')),
    url(r'^clients/', include('clients.urls', namespace='clients')),
    url(r'^invoices/', include('invoices.urls', namespace='invoices')),
    url(r'^auth/', include('auth.urls', namespace='auth')),
    url(r'^auth/logout', include('auth.urls')),
)
