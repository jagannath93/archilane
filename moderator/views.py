from django.contrib.auth.models import User
from moderator.models import Moderator, Moderations
from forum.models import Topic
from site_auth.models import UserProfile

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

def distribution(request):
	to_be_moderated = Topic.objects.filter(is_moderated=False)
	user_moderators = UserProfile.objects.filter(user_level=3)	# moderator_level =3
	
	for moderator in user_moderators and topic in to_be_moderated:
		if moderator.items_to_be_moderated < 5:			# max_limit is set to 5
  			m = Moderations(moderator, topic)
			m.save()


	
