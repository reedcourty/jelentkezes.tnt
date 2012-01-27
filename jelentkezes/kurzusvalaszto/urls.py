from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('kurzusvalaszto.views',
    url(r'^$', 'index'),
    url(r'^user/', 'user_start'),
    url(r'^username/', 'name_load'),
    url(r'^kurzusvalasztas/', 'kurzusvalasztas'),
)