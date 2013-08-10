from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

NOTIFICATION_TYPES = (
	('PR', 'private'),
	('PU', 'public'),
	('AN', 'announcement'),
	('EV', 'event'),
)

NOTIFICATION_STATES = (
	('AC', 'active'),
	('BL', 'blocked'),
	('RA', 'report_abuse'),
)

class Notification(models.Model):
	ntfnId = models.CharField(max_length=35, blank=True)
	module = models.CharField(max_length=30)
	key = models.IntegerField(max_length=5, default = -1) #Need to change: max_length - max 5 digits b'coz pk can be larger than this.
	model = models.CharField(max_length=25, blank=True)
	app = models.CharField(max_length=30, blank=True)
	url = models.URLField(blank=True, null=True)
	type = models.CharField(max_length=2, choices=NOTIFICATION_TYPES, default='PR')
	state = models.CharField(max_length=2, choices=NOTIFICATION_STATES, default='AC')
	timestamp = models.DateTimeField(auto_now=True)
	receivers = models.ManyToManyField('Receiver')

	class Meta:
		ordering = ['-timestamp']
	def __unicode__(self):
		return str(self.content)


	@staticmethod
	def save_notification(module, key, url, app, model, type, receivers=[]):
		ntfnId = ''
		ntfn = Notification(ntfnId=ntfnId, module=module, key=key, url=url, app=app, model = "Portfolio" if model else '')
		ntfn.save()
		import hashlib
		m = hashlib.md5()
		m.update(str(ntfn.pk))
		ntfn.ntfnId = m.hexdigest()
		#if type == "private":
		receivers = map(lambda user: Receiver.objects.get_or_create(user=user)[0], receivers)
		ntfn.receivers.add(*receivers)
		ntfn.save()
		return ntfn

	@staticmethod
	def delete_notification(ntfnId):
		try:
			ntfn = Notification.objects.get(ntfnId=ntfnId)
			ntfn.delete()
		except Exception as e:
			print "Error: ", e


class Receiver(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	
	def __unicode__(self):
		return str(self.user)
	
