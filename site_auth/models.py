from django.db import models
from django.contrib.auth.models import User

#class Group(models.Model):
#	name = models.CharField(max_length=20, choices=GROUP_CHOICES)
			

class UserProfile(models.Model):
	GENDER_CHOICES = (
		(u'M',u'Male'),
		(u'F',u'Female'),
	)

	'''
	GROUP_CHOICES = (
	(u'P', u'Professional'),
	(u'S', u'Student'),
	)
	'''	
	user = models.OneToOneField(User)
	#group = models.CharField(max_length=20, choices=GROUP_CHOICES)

	friend = models.ManyToManyField('self', through = 'FriendRelations', symmetrical = False, related_name = 'friends')
	following = models.ManyToManyField('self', through = 'FollowRelations', symmetrical = False, related_name = 'people_following')

	designation = models.CharField(max_length=5)
	is_verified = models.BooleanField(default = False)
	is_new_user = models.BooleanField(default = True)
	gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
	dob = models.DateField()
	college = models.CharField(max_length='30')
	course = models.CharField(max_length='30')
	year = models.IntegerField(max_length='2')
	image = models.ImageField(upload_to = "profile_pics/", default = "profile_pics/default_profile_pic.jpg")

	def __unicode__(self):
		return self.user.username

	def add_friend(self, uprofile, status):
		relationship, created = FriendRelations.objects.get_or_create(
			from_person = self,
			to_person = uprofile,
			status = status)
		relationship, created = FriendRelations.objects.get_or_create(
			from_person = uprofile,
			to_person = self,
			status = status)
		return relationship

	def remove_friend(self,uprofile,status):
		FriendRelations.objects.filter(
			from_person = self,
			to_person = uprofile,
			status = status).delete()
		FriendRelations.objects.filter(
			from_person = uprofile,
			to_person = self,
			status = status).delete()
		return

	def block_friend(self, uprofile, status):
		FriendRelations.objects.get(
			from_person = self,
			to_person = uprofile,
			status = status).status = BLOCKED 
		FriendRelations.objects.get(
			From_person = uprofile,
			to_person = self,
			status = status).status = BLOCKED 
		return relationship

	def get_friends (self, status):
		return self.friend.filter(
			friend_to_persons__status = status,
			friend_to_persons__from_person = self)

	def is_friend (self, other):
		if FriendRelations.objects.get(
			from_person = self,
			to_person = other) is not None:
			return True
		else:
			return False
		
	def get_one_deg_users(self,status):
		friends = self.get_friends(status)
		one_deg_users = []

		for friend in friends:
			friends_of_friend = friend.get_friends(status)
			for friend_of_friend in friends_of_friend:
				if len(FriendRelations.objects.filter(
					from_person = self,
					to_person = friend_of_friend)) == 0 and friend_of_friend.pk != self.pk:
						one_deg_users.append(friend_of_friend)
		return one_deg_users
	'''
	def block_one_deg_users(self.status):
		one_deg_users = self.get_one_deg_users(status)
		for one_deg_user in one_deg_users:
			FriendRelations.objects.get(
				from_person
				)'''
			
        def add_following(self, uprofile, status):
                relationship, created = FollowRelations.objects.get_or_create(
                        from_person = self,
                        to_person = uprofile,
                        status = status)
                return relationship

        def remove_follower(self, uprofile,status):
                FollowRelations.objects.filter(
                        from_person = self,
                        to_person = uprofile,
                        status = status).delete
                return

        def get_followers (self, status):
                return self.following.filter(
                        following_to_persons__status = status,
                        following_to_persons__from_person = self)

	def get_followers (self, status):
		return self.people_following.filter(
			following_from_persons__status = status,
			following_from_persons__to_person = self)

class SignupData(models.Model):
	user = models.OneToOneField(User)
	activation_key = models.CharField(max_length=70)
	key_expires = models.DateTimeField()

FRIEND = 1
FOLLOWING = 2
BLOCKED = 3

FRIENDSHIP_STATUS = (
(FRIEND, 'Friend'),
(BLOCKED, 'Blocked'),
)

FOLLOWING_STATUS = (
(FOLLOWING, 'Following'),
(BLOCKED, 'Blocked'),
)


class FriendRelations(models.Model):
	from_person = models.ForeignKey(UserProfile, related_name = 'friend_from_persons')
	to_person = models.ForeignKey(UserProfile, related_name = 'friend_to_persons')
	status = models.IntegerField(choices = FRIENDSHIP_STATUS)


class FollowRelations(models.Model):
	from_person = models.ForeignKey(UserProfile, related_name = 'following_from_persons')
	to_person = models.ForeignKey(UserProfile, related_name = 'following_to_persons')
	status = models.IntegerField(choices = FOLLOWING_STATUS)

