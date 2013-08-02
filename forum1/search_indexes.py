from haystack.indexes import *
from haystack import site
from forum.models import Topic, Post, Reply

class TopicIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	name = CharField(model_attr='topic_name')
	desc = CharField(model_attr='topic_desc')
	def index_queryset(self):
		return Topic.objects.all()

site.register(Topic, TopicIndex) 

class PostIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	name = CharField(model_attr='post_content')

	def index_queryset(self):
		return Post.objects.all()

site.register(Post, PostIndex) 

class ReplyIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	name = CharField(model_attr='reply_content')

	def index_queryset(self):
		return Reply.objects.all()

site.register(Reply, ReplyIndex) 


