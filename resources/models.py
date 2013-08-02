from django.db import models

class Resource(models.Model):
	GROUP_CHOICES = (
		(u'1',u'Public'),
		(u'2',u'Friends'),
		(u'3',u'Networks'),
		(u'4',u'Me'),		
	)
	Title = models.CharField(max_length=20)
	des = models.TextField()
	item = models.FileField(upload_to='media/')
	is_verified = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	permitted_group = models.CharField(max_length=2, choices = GROUP_CHOICES,)
	points = models.IntegerField(max_length=3, default=0)


