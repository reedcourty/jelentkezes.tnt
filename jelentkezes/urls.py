from django.conf.urls.defaults import patterns, include, url

from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

admin_url = settings.ADMIN_URL

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jelentkezes.views.home', name='home'),
    # url(r'^jelentkezes/', include('jelentkezes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^' + admin_url, include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'', include('kurzusvalaszto.urls')),
)
