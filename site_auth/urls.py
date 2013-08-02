from django.conf.urls import patterns, include, url

urlpatterns = patterns('site_auth.views',
	(r'','index'),
	(r'^signup/$','signup'),
	(r'^signin/$','signin'),
	(r'^signout/$', 'signout'),
	(r'^login/$', 'login'),

)
