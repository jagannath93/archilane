from haystack.query import SearchQuerySet
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson
from django.core import serializers
from forum.models import Topic, Post, Reply

def search(request):
	return render_to_response('search/apple.html') #, Request_Context = context_instance(request))


def global_search(request):
	if request.is_ajax():
			data = request.GET["q"]
			forum_topics = SearchQuerySet().models(Topic).filter(content=data)
			forum_posts = SearchQuerySet().models(Post).filter(content=data)
			forum_replies = SearchQuerySet().models(Reply).filter(content=data)
			forum_results = len(forum_topics) + len(forum_posts) + len(forum_replies)
	
			results = {}
			results['forum_topics'] = [result.name for result in forum_topics]
		 	results['forum_topic_results'] = len(forum_topics)
			results['forum_posts'] = [result.name for result in forum_posts]
			results['forum_post_results'] = len(forum_posts)
			results['forum_replies'] = [result.name for result in forum_replies]
			results['forum_reply_results'] = len(forum_replies)
			results['forum_results'] = forum_results
			json = simplejson.dumps(results)
			print(json)  # just for testimg
			import time
			time.sleep(1)
			return HttpResponse(json, mimetype='application/json')  # 'JSON' Response
	else:
		return HttpResponse("Not ajax!!")


