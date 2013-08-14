from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	name = models.CharField(max_length=30)
	des = models.CharField(max_length=100)
	color = models.CharField(max_length=10)
	feeds = models.IntegerField(max_length=4, default=0)  #This will give number of feeds in that category. ### Need to change datatype to double.
	
	def __unicode__(self):	
		return self.name

class AFeedUser(models.Model):
	user = models.OneToOneField(User)
	frequency = models.IntegerField(max_length=3, default=0)
	categories = models.ManyToManyField(Category)				
	
	def __unicode__(self):
		return self.user


class ArchiFeed(models.Model):
	category = models.ForeignKey(Category, related_name='feed_category')
	title = models.CharField(max_length=100)
	des = models.TextField()
	has_image = models.BooleanField(default=1)
	image_path = models.CharField(max_length=70, default='')
	#item = models.TextField()
	pub_date = models.CharField(max_length=10)
	#channel = models.CharField(max_length=20)
	source = models.CharField(max_length=30)
	link = models.CharField(max_length=200)

	def __unicode__(self):
		return self.title

"""
class ArchifeedUser(models.Model):
	user = models.OnetoOneField(User)
	Category = models.ManyToManyField(Category)

	def __unicode__(self):	
		return self.user
"""
'''
class related_news(models.Model):
  item = models.ManyToManyField(news_feeds)
  main_item = models.ForeignKey(news_feeds, related_name="main_items")
  related_items = models.ForeignKey(news_feeds, related_name="related_names") '''
