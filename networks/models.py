from django.db import models
from django.contrib.auth.models import User


PENDING = 1
SEEN = 2
BLOCKED = 3

status_choices = (
	(PENDING, 'Pending'),
	(SEEN, 'Seen'),
	(BLOCKED, 'Blocked'),	
)

class Notification(models.Model):
	from_user = models.ForeignKey(User, related_name="notify_from")
	to_user = models.ForeignKey(User, related_name="notify_to")
	status = models.IntegerField(choices = status_choices)

	def __unicode__(self):
		return self.status
		
