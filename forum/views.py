from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import context, RequestContext
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.contrib.auth.models import User
from forum.models import Category
from forum.models import Topic
from forum.models import Post
from forum.models import Reply
from site_auth.models import UserProfile
from notifications.models import *
from django.contrib.auth import authenticate, login, logout

@login_required
def home(request):	# login_field	
	categories = Category.objects.all()
	groups = categories.values("cat_group").distinct()	
	latest_topics = Topic.objects.order_by("-topic_date" )
	#top_topics = Topic.objects.order_by("topic_views" )[:5]
	#active_topics = Topic.objects.order_by("topic_active" )[:5]

#	return render_to_response ('forum/home.html', {'latest_threads':latest_threads},
#			{'top_threads':top_threads},{'active_threads':active_threads},	context_instance=RequestContext(request))
	return render_to_response ('forum/home.html',{'categories':categories, 'groups':groups, "latest_topics":latest_topics} 
					, context_instance=RequestContext(request))
@login_required
def latest_topics(request):
	if request.is_ajax():
		latest_topics = Topic.objects.order_by("-topic_date")
		return render_to_response('forum/latest_topics.html', {"latest_topics":latest_topics}, context_instance=RequestContext(request))
	elif request.method == "GET":
		categories = Category.objects.all()
		groups = categories.values("cat_group").distinct()
		latest_topics = Topic.objects.order_by("-topic_date")		
		data={
		  'categories':categories,
		  'groups':groups,
		  'latest_topics':latest_topics,
		}	
		return render_to_response('forum/latest_topics_page.html', data, context_instance=RequestContext(request))


@login_required
def active_topics(request):
	if request.is_ajax():
		active_topics = Topic.objects.order_by("topic_name")
		return render_to_response('forum/active_topics.html', {"active_topics":active_topics}, context_instance=RequestContext(request))
	elif request.method == "GET":
		categories = Category.objects.all()
		groups = categories.values("cat_group").distinct()
		active_topics = Topic.objects.order_by("topic_name")
		data={
		  'categories':categories,
		  'groups':groups,
		  'active_topics':active_topics,
		}	
		return render_to_response('forum/active_topics_page.html', data, context_instance=RequestContext(request))
		
@login_required
def my_activity(request):
	if request.is_ajax():
		topics_activity = Topic.objects.filter(topic_by = request.user)
		posts_activity = Post.objects.filter(post_by = request.user)
		replies_activity = Reply.objects.filter(reply_by = request.user)
		data={
		  'topics_activity' : topics_activity,
		  'posts_activity' : posts_activity,
		  'replies_activity' : replies_activity,
		}
		return render_to_response('forum/my_activity.html', data, context_instance=RequestContext(request))
	elif request.method == "GET":
		categories = Category.objects.all()
		groups = categories.values("cat_group").distinct()
		topics_activity = Topic.objects.filter(topic_by = request.user)
		posts_activity = Post.objects.filter(post_by = request.user)
		replies_activity = Reply.objects.filter(reply_by = request.user)
		data={
		  'topics_activity' : topics_activity,
		  'posts_activity' : posts_activity,
		  'replies_activity' : replies_activity,
		  'categories':categories,
		  'groups':groups,
		}	
		return render_to_response('forum/my_activity_page.html', data, context_instance=RequestContext(request))


@login_required
def add_topic(request):
	t1 = Topic (topic_cat_id= request.POST['category'], topic_by_id=request.user.id, topic_date=timezone.now(),
				topic_name=request.POST['topic_name'],topic_desc=request.POST['topic_desc'],
					 topic_views='0', topic_stars='0', topic_active='0')
	t1.save()
	if not request.user in t1.topic_subscribers.all():
		t1.topic_subscribers.add(request.user)  # Topic subscriptions
		t1.subscribes += 1
		t1.save()
	content = "New topic Posted : "+ t1.topic_name +" by -"+ str(request.user)
	url = "http://test.archilane.com/forum/topic/" + str(t1.id)
	topic_subscribers = t1.topic_subscribers.all()
	Notification.save_notification(content,url,'forum','Topic','private',topic_subscribers)
	if t1.topic_cat.subscribes > 0:
		cat_subscribers = t1.topic_cat.cat_subscribers.all()
		Notification.save_notification(content,url,'forum','Category','private',cat_subscribers)
	return HttpResponse(t1.pk)
	#return HttpResponseRedirect("/forum/topic/%s" % t1.id)

@login_required
def add_post(request):
	p1 = Post (post_topic_id = request.POST['topic'], post_by_id=request.user.id , 
			post_date=timezone.now(), post_content=request.POST['post_content'])
	p1.save()
	t = p1.post_topic
	if not request.user in t.topic_subscribers.all():
		t.topic_subscribers.add(request.user)  # Topic subscriptions
		t.subscribes += 1
		t.save()
	content = "New post on : "+ t.topic_name +" by -"+ str(request.user) +"\n"+ p1.post_content
	url = "http://test.archilane.com/forum/topic/" + str(t.id)
	topic_subscribers = t.topic_subscribers.all()
	Notification.save_notification(content,url,'forum','Post','private',topic_subscribers)
	if t.topic_cat.subscribes > 0:
		cat_subscribers = t.topic_cat.cat_subscribers.all()
		Notification.save_notification(content,url,'forum','Category','private',cat_subscribers)

	#print(p1.post_topic.pk)	
	#topic(request, p1.post_topic.pk)
	return HttpResponse(p1.post_topic.pk)
	#return HttpResponseRedirect ("/forum/topic/%s" % request.POST['topic'])

@login_required
def topic(request, topic_id):
	if request.is_ajax():
		#name = request.GET.get('topic')
		topic = get_object_or_404(Topic, pk=topic_id)
		posts = Post.objects.filter(post_topic_id=topic_id)
		user_profile = UserProfile.objects.get(user=request.user) # Remove if unnecessary
		#return HttpResponse (posts)
		var = {}
		for post in posts:
			replies= Reply.objects.filter(reply_post_id=post.pk)
			var[post.pk] = replies
		return render_to_response ('forum/topic.html',{'posts':posts, 'topic_id':topic_id, 'user_profile':user_profile,
						'replies':var, 'topic':topic}, context_instance=RequestContext(request))
	elif request.method == "GET":
		categories = Category.objects.all()
		groups = categories.values("cat_group").distinct()
		topic = get_object_or_404(Topic, pk=topic_id)
		posts = Post.objects.filter(post_topic_id=topic_id)
		user_profile = UserProfile.objects.get(user=request.user) # Remove if unnecessary
		#return HttpResponse (posts)
		var = {}
		for post in posts:
			replies= Reply.objects.filter(reply_post_id=post.pk)
			var[post.pk] = replies
		data = {
		  'categories':categories,
		  'groups':groups,
		  'posts':posts,
		  'topic_id':topic_id,
		  'user_profile':user_profile,
		  'replies':var,
		  'topic':topic,
		}	
		return render_to_response('forum/topic_page.html', data, context_instance=RequestContext(request))


@login_required
def category(request):
	if request.is_ajax():
		cat = request.GET.get('cat')
		category = Category.objects.get(cat_name=cat)
		topics= Topic.objects.filter(topic_cat = category.pk)
		
		topic_replies_num = {}
		posts_num = 0
		replies_num = 0
		for topic in topics:
			posts = Post.objects.filter(post_topic_id = topic.pk)
			posts_num = posts.count()
			for post in posts:
				replies_num = Reply.objects.filter(reply_post = post.pk).count()
			topic_replies_num[topic.pk] = posts_num + replies_num			 

		data={
		   'topics' : topics,
		   'category' : category,
		   'replies_num' : topic_replies_num,
		}	
		#return HttpResponse(post[0].post_content)
		import time
		time.sleep(1)
		return	render_to_response('forum/category.html', data)
		
	elif request.method == "GET":
		categories = Category.objects.all()
		groups = categories.values("cat_group").distinct()
		cat = request.GET.get('cat')
		category = Category.objects.get(cat_name=cat)
		topics= Topic.objects.filter(topic_cat = category.pk)
		
		topic_replies_num = {}
		posts_num = 0
		replies_num = 0
		for topic in topics:
			posts = Post.objects.filter(post_topic_id = topic.pk)
			posts_num = posts.count()
			for post in posts:
				replies_num = Reply.objects.filter(reply_post = post.pk).count()
			topic_replies_num[topic.pk] = posts_num + replies_num			 
		
		if request.user in category.cat_subscribers.all():
			is_subscribed = 1
		else:
			is_subscribed = 0

		data={
		  'categories':categories,
		  'is_subscribed':is_subscribed,
		  'groups':groups,
		   'topics' : topics,
		   'category' : category,
		   'replies_num' : topic_replies_num,
		}	
		#return HttpResponse(is)
		return render_to_response('forum/category_page.html', data, context_instance=RequestContext(request))

	
 
@login_required
def add_reply (request):
	#if request.method == "POST":
	post_id = request.POST['post_id']
	#print("post_id= "+post_id)
	r=Reply(reply_date=timezone.now(), reply_by_id=request.user.id, 
	reply_post_id=post_id, reply_content=request.POST['reply_content'])
	r.save()
	p = r.reply_post
	t = p.post_topic
	if not request.user in t.topic_subscribers.all():
		t.topic_subscribers.add(request.user)  # Topic subscriptions
		t.subscribes += 1
		t.save()
	content = str(request.user) + " replied: "+ r.reply_content +" - on post "+ p.post_content
	url = "http://test.archilane.com/forum/topic/" + str(t.id)
	topic_subscribers = t.topic_subscribers.all()
	Notification.save_notification(content,url,'forum','Post','private',topic_subscribers)
	if t.topic_cat.subscribes > 0:
		cat_subscribers = t.topic_cat.cat_subscribers.all()
		Notification.save_notification(content,url,'forum','Category','private',cat_subscribers)
	#topic_id = Post.objects.get(pk=post_id).post_topic_id
	#return HttpResponseRedirect ("/forum/topic/%s" % topic_id)
	#print(r.reply_post.pk)
	#print(r.reply_post.post_topic.pk)
	return HttpResponse(r.reply_post.post_topic.pk)
	#else:
	#	return HttpResponse("fail")
	
@login_required
def topic_subscription(request):
	topic_id = request.GET['topic']
	t = Topic.objects.get(pk=topic_id)
	subscribers = t.topic_subscribers.all()
	if not request.user in subscribers:
		t.topic_subscribers.add(request.user)
		t.subscribes += 1
		t.save()
	return HttpResponse(t.subscribes)

@login_required
def topic_unsubscription(request):
	topic_id = request.GET['topic']
	t = Topic.objects.get(pk=topic_id)
	subscribers = t.topic_subscribers.all()
	if request.user in subscribers:
		t.topic_subscribers.remove(request.user)
		t.subscribes -= 1
		t.save()
	return HttpResponse(t.subscribes)

@login_required
def cat_subscription(request):
	cat_id = request.GET['cat']
	c = Category.objects.get(pk=cat_id)
	cat_subscribers = c.cat_subscribers.all()
	if not request.user in cat_subscribers:
		c.cat_subscribers.add(request.user)
		c.subscribes += 1
		c.save()
	return HttpResponse(c.subscribes)

@login_required
def cat_unsubscription(request):
	cat_id = request.GET['cat']
	c = Category.objects.get(pk=cat_id)
	cat_subscribers = c.cat_subscribers.all()
	if request.user in cat_subscribers:
		c.cat_subscribers.remove(request.user)
		c.subscribes -= 1
		c.save()
	return HttpResponse(c.subscribes)
		
		
