from django.db import models
from django.contrib.auth.models import User
from forum.models import Topic

class Moderations(models.Model):
	mod_id=models.ForeignKey(User, related_name ="mod_id")
	mod_topic=models.ForeignKey(Topic)

class Moderator(models.Model):
	mod_id=models.ForeignKey(User, related_name = "mod_user")
	mod_activity=models.IntegerField()
	items_moderated=models.IntegerField(max_length = 5)
	items_to_be_moderated=models.IntegerField(max_length = 5)
	date_joined = models.DateTimeField()
	
	def __unicode__(self):
		return self.mod_user
