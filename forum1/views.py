# django imports
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import context, RequestContext
from django.contrib.auth.decorators import login_required

# python imports
import datetime

# model imports 
from django.contrib.auth.models import User
from forum.models import Category
from forum.models import Topic
from forum.models import Post
from forum.models import Reply
from django.contrib.auth import authenticate, login, logout

@login_required
def home(request):	# User home page
	categories = Category.objects.all()

	latest_topics = Topic.objects.order_by("-topic_date" )[:5]
	top_topics = Topic.objects.order_by("topic_views" )[:5]
	active_topics = Topic.objects.order_by("topic_active" )[:5]
	return render_to_response ('forum/home.html',{'categories':categories, "latest_topics":latest_topics, 
					"top_topics":top_topics, "active_topics":active_topics},	context_instance=RequestContext(request))

@login_required
def add_topic(request):
	t1 = Topic (topic_cat_id= request.POST['category'], topic_by_id=request.user.id, topic_date=datetime.datetime.now(),#timezone.now(),
				topic_name=request.POST['topic_name'],topic_desc=request.POST['topic_desc'],
					 topic_views='0', topic_stars='0', topic_active='0')
	t1.save()
	return HttpResponseRedirect("/forum/topic/%d" % t1.id)

@login_required
de