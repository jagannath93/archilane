from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	cat_name = models.CharField(max_length=25)
	cat_desc = models.CharField(max_length=50)
	cat_group = models.CharField(max_length=30)	
	cat_subscribers = models.ManyToManyField(User, related_name='cat+')
	subscribes = models.IntegerField(max_length=5, default=0, blank=True)

	def __unicode__(self):
		return self.cat_name
	class Meta:
		ordering = ["cat_group"]  # changed from cat_name.

class Topic(models.Model):
	topic_cat = models.ForeignKey(Category, related_name = "topic_cat")
	topic_by = models.ForeignKey(User, related_name = "topic_by")
	topic_date = models.DateTimeField()
	topic_name = models.CharField(max_length='40')
	topic_desc = models.TextField()
	topic_views = models.IntegerField()
	topic_stars = models.DecimalField(max_digits=3, decimal_places=2)
	topic_active = models.DecimalField(max_digits=3, decimal_places=2)
	is_moderated = models.BooleanField(default = 0)
	is_active = models.BooleanField(default = True)
	topic_subscribers = models.ManyToManyField(User, related_name='topic+')
	subscribes = models.IntegerField(max_length=5, default=0, blank=True)
	
	def __unicode__(self):
		return self.topic_name

class Post(models.Model):							#this is actual reply
	post_topic = models.ForeignKey(Topic, related_name = "post_topic", on_delete = models.CASCADE)
	post_by = models.ForeignKey(User, related_name = "post_by")
	post_date = models.DateTimeField()
	post_content = models.TextField()
	is_moderated = models.BooleanField(default=0)
	is_active = models.BooleanField(default = True)

class Reply(models.Model):							#this is reply to a reply
	reply_date = models.DateTimeField()
	reply_post = models.ForeignKey(Post, related_name = "reply_post", on_delete = models.CASCADE)
	reply_content = models.TextField()
	reply_by = models.ForeignKey(User, related_name = "reply_by")
	is_moderated = models.BooleanField(default=0)
	is_active = models.BooleanField(default = True)

class Topic_Viewer (models.Model):
	viewer_id = models.ForeignKey(Topic)
	viewer_count = models.IntegerField(max_length=1)

