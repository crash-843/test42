from django.conf.urls import patterns, url

urlpatterns = patterns(
    'core.views',
    url(r'^$', 'index', name='index'),
    url(r'^log/$', 'get_http_log', name='log'),
)
