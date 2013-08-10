from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^site_auth/signup/$', 'site_auth.views.signup'),
	(r'^home/$', 'site_auth.views.home'),
	(r'^signup/(?P<activation_key>\w+)/$','site_auth.views.account_confirmation'),
	(r'^site_auth/signin/$', 'site_auth.views.signin'),
	(r'^logout/$', 'site_auth.views.signout'),
	(r'^site_auth/login/$', 'site_auth.views.login'),
	(r'^site_auth/upload_pic/$', 'site_auth.views.upload_pic'),
	#(r'^forum/$', 'forum.views.home'),
	#(r'^forum/add_topic/$', 'forum.views.add_topic'),
	#(r'^forum/topic/(?P<topic_id>\d+)/$', 'foload_picrum.views.topic'),
	#(r'^forum/add_reply/$', 'forum.views.add_reply'),
	#(r'^forum/add_post/$', 'forum.views.add_post'),
#	(r'^site_auth/search/$', include('haystack.urls')),
	#(r'^ajax/$', 'ajax.views.index'),
	#(r'^ajax/nav/(?P<c_id>\w+)/$', 'ajax.views.get_navigation'),
	#(r'^ajax/con/(?P<c_id>\w+)/$', 'ajax.views.get_content'),
	#(r'^search/$', 'search.views.search'),
	#(r'^search/global/$' ,'search.views.global_search'),

#portfolio:
	#(r'^portfolio/$', 'portfolio.views.home'),
	
#notifications
	(r'^notifications/', 'notifications.views.home'),


#archifeed
	(r'^archifeed/extract/$', 'archifeed.views.data_extractor'),
	(r'^archifeed/$', 'archifeed.views.archifeed'),
	(r'^archifeed/settings/$', 'archifeed.views.settings'),

	(r'^portfolio/(?P<user_id>\d+)/$', 'portfolio.views.home'),
	(r'^portfolio/(?P<owner_id>\d+)/(?P<token>\d+)/$', 'portfolio.views.mark_portfolio'),
	(r'^portfolio/item/(?P<item_id>\d+)/(?P<token>\d+)/$', 'portfolio.views.mark_portfolio_item'),
	(r'^portfolio/likes/(?P<user_id>\d+)/$', 'portfolio.views.fetch_likes'),
	(r'^portfolio/update_groups/$', 'portfolio.views.update_groups'),
	(r'^portfolio/update_items/$', 'portfolio.views.update_items'),
	(r'^portfolio/move_items/$', 'portfolio.views.move_items'),
	#(r'^portfolio/add_group/$', 'portfolio.views.add_group'),
	(r'^portfolio/item/upload/$', 'portfolio.views.add_new_item'),
	(r'^portfolio/add_item/$', 'portfolio.views.add_item'),
	(r'^portfolio/item/(?P<item_id>\d+)/$', 'portfolio.views.portfolio_item'),


#networks:
	(r'^networks/$','networks.views.home'),
	(r'^networks/add_friend/(?P<friend_id>\d+)/$','networks.views.add_friend'),
	(r'^networks/del_friend/(?P<friend_id>\d+)/$','networks.views.del_friend'),
	#(r'^networks/add_following/(?P<following_id>\d+)/$','networks.views.add_following'),
	#(r'^networks/del_following/(?P<following_id>\d+)/$','networks.views.del_following'),

#messages:
	(r'^messages/$','messages.views.home'),

#forum:	
	(r'^forum/$', 'forum.views.home'),
	#(r'^forum/navigation/$', 'forum.views.navigation'),
	#(r'^forum/main_content/$', 'forum.views.home'),
	(r'^forum/latest_topics/$', 'forum.views.latest_topics'),
	(r'^forum/active_topics/$', 'forum.views.active_topics'),
	(r'^forum/my_activity/$', 'forum.views.my_activity'),
	(r'^forum/topic/(?P<topic_id>\d+)$', 'forum.views.topic'),
	#(r'^forum/topic/(?P<topic_id>\d+)/post/(?P<post_id>\d+)$', 'forum.views.post'),
	(r'^forum/add_topic/$', 'forum.views.add_topic'),
	(r'^forum/add_post/$', 'forum.views.add_post'),	
	(r'^forum/add_reply/$', 'forum.views.add_reply'),	
	(r'^forum/category/$', 'forum.views.category'),
	(r'^forum/category/subscribe/$', 'forum.views.cat_subscription'),
	(r'^forum/category/unsubscribe/$', 'forum.views.cat_unsubscription'),
	(r'^forum/topic/subscribe/$', 'forum.views.topic_subscription'),
	(r'^forum/topic/unsubscribe/$', 'forum.views.topic_unsubscription'),
	
	(r'^resources/$', 'resources.views.response_mimetype'),
	#('^uploadurl$', 'resources.views.FileHandler'),	

	
    # Examples:
    # url(r'^$', 'archilane.views.home', name='home'),
    # url(r'^archilane/', include('archilane.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


import os
urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media')}),
)


from archilane.settings import DEBUG
if DEBUG:
	urlpatterns += patterns('', (
        r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': 'static'}),

	(r'^media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': 'media'}
    ),)



'''
#moderator:

#approve
	(r'^moderator/(?P<topic_id>\d+)/approve/$', 'moderator.views.approve'),	
	(r'^moderator/(?P<topic_id>\d+)/(?P<post_id>\d+)/approve/$', 'moderator.views.approve'),
	(r'^moderator/(?P<topic_id>\d+)/(?P<post_id>\d+)/(?P<reply_id>\d+)/approve/$', 'moderator.views.approve'),
#edit
	(r'^moderator/(?P<topic_id>\d+)/edit/$', 'moderator.views.edit'),	
	(r'^moderator/(?P<topic_id>\d+)/(?P<post_id>\d+)/edit/$', 'moderator.views.edit'),
	(r'^moderator/(?P<topic_id>\d+)/(?P<post_id>\d+)/(?P<reply_id>\d+)/edit/$', 'moderator.views.edit'),
#delete
	(r'^moderator/(?P<topic_id>\d+)/delete/$', 'moderator.views.delete'),	
	(r'^moderator/(?P<topic_id>\d+)/(?P<post_id>\d+)/delete/$', 'moderator.views.delete'),
	(r'^moderator/(?P<topic_id>\d+)/(?P<post_id>\d+)/(?P<reply_id>\d+)/delete/$', 'moderator.views.delete'),

'''




