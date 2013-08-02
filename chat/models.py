from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
	data = models.CharField(max_length=500)
	user = models.ForeignKey(User)

