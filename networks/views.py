from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from models import Notification
from site_auth.models import UserProfile
from site_auth.models import FriendRelations, FollowRelations
from site_auth.models import FRIENDSHIP_STATUS

def home(request):
	not_friends = []
	all_users = UserProfile.objects.all()
	self_userprofile = get_object_or_404(UserProfile, user = request.user.id)

#	for user in all_users:
#		if UserProfile.is_friend(self_userprofile, user):
#			continue
#		else:
#			not_friends.append(user)
#	not_friends = UserProfile.objects.all()
#	friends = FriendRelations.objects.filter(from_person = request.user)
        self_user = get_object_or_404(UserProfile, user = request.user.id)
	friends = UserProfile.get_friends(self_user, 1)

	following = FollowRelations.objects.filter(from_person  = request.user.id)
	followers = FollowRelations.objects.filter(to_person = request.user.id)

        return render_to_response("networks/home.html", {
							'all_users':all_users,
#                                                        'not_friends': not_friends,
                                                        'friends': friends,
                                                        'following': following,
                                                        'followers': followers
                                                        },
                                                                context_instance = RequestContext(request))

def add_friend(request, friend_id):
        self_user = get_object_or_404(UserProfile, user = request.user.id)
	friend = get_object_or_404(UserProfile, user_id = friend_id)

	UserProfile.add_friend(self_user, friend, 1)
#	print (a.to_person)
	return HttpResponse(friend)

def del_friend(request, friend_id):
        self_user = get_object_or_404(UserProfile, user = request.user.id)
        friend = get_object_or_404(UserProfile, user_id = friend_id)

        UserProfile.remove_friend(self_user, friend, 1)
        return HttpResponse("Done..deleted succesfully")

