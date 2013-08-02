from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
import random, sha, datetime
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.views import password_reset
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from site_auth.models import UserProfile, SignupData
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from site_auth.forms import SignupForm, SigninForm, UploadPicForm

@login_required
def home(request):  #User home page.
	profile =  UserProfile.objects.get(user = request.user)
	dummy_user = User.objects.get(pk = 1)
	#print(profile)
	#self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
	return render_to_response("user/home.html", {'profile':profile,'dummy_user':dummy_user}, context_instance = RequestContext(request))

def signup(request):
	next_page = request.POST.get('next', None)
	if request.user.is_authenticated():
		return HttpResponseRedirect('/home/')
	if request.method == 'POST':
		print("As post")
		new_data = request.POST.copy()
		form = SignupForm(new_data)
		print("data binded to form")
		if form.errors:
			print(form.errors)
		if form.is_valid():
			print("valid form.")
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			email = form.cleaned_data['email']
			designation = form.cleaned_data['designation']
			gender = form.cleaned_data['gender']
			dob = form.cleaned_data['dob']
			college = form.cleaned_data['college']
			course = form.cleaned_data['course']
			year = form.cleaned_data['year']

			print(email)
			# if there are no form or field errors:
			if form.errors is None or len(form.errors) <= 0:	
				new_user = form.save(new_data)
				new_user.is_active = False
				new_user.save()
#				User.objects.create_user()

				print(new_user.username)
				print(new_user.email)	
				print(new_user.password)
				print(new_data["email"])
				print(new_data["course"])			
				
				# Generating account activation key 
				salt = sha.new(str(random.random())).hexdigest()[:5]
				activation_key = sha.new(salt+new_user.email).hexdigest()
				key_expires = timezone.now() + datetime.timedelta(1)
				new_profile = UserProfile(user=new_user, gender=gender, dob=dob, college=college, course=course, year=year)
				new_signup_data = SignupData(user=new_user, activation_key=activation_key, key_expires=key_expires)
				new_profile.save()
		
				# sending key to user's email account

				#try:
				subject = 'Archilane.com account confirmation'
				from_email = 'team@archilane.com'	
			
				text_content = "Account confirmation mail</br>"
				html_content = "<p>To activate your account click on this link within<span style='color:red;'>24 hours</span>:<a href='http://test.archilane.com/signup/%s'>www.archilane.com/signup/%s</a></p>"%(new_signup_data.activation_key,new_signup_data.activation_key)
				email = EmailMultiAlternatives(subject, text_content, from_email, [new_user.email])
				
				email.attach_alternative(html_content, 'text/html')
				
				print(email)

				if email.send():
					print("email.send()")
					new_signup_data.save()
					return render_to_response('frontend/landing_page/mail_sent.html', context_instance=RequestContext(request))	
				else:
					return render_to_response('login_form/retry_email_sending.html', context_instance=RequestContext(request))		
				#except: return render_to_response('login_form/email_sending_failed.html', context_instance=RequestContext(request))
				

				return HttpResponseRedirect('/site_auth/signin/')
			else:
				message = "Signup errors"
				return render_to_response('frontend/landing_page/landing_page.html',{'message':message}, context_instance = RequestContext(request))		
		else:
			message = "Invalid form"
			return render_to_response('frontend/landing_page/landing_page.html', {'message':message}, context_instance = RequestContext(request))
		#form = SignupForm()
	return render_to_response('frontend/landing_page/landing_page.html', context_instance = RequestContext(request))


def account_confirmation(request, activation_key):
	if request.user.is_authenticated():
                return HttpResponseRedirect('/home/')


	
	signup_data = get_object_or_404(SignupData, activation_key=activation_key)
	
	if signup_data.key_expires < timezone.now():
		print("key_expired!!")
		return render_to_response('login_form/confirm.html',{'key_expires' : True}, context_instance=RequestContext(request))
	#else:
		#return HttpResponse("Your confirmation key has expired!!")
		

	user_account = signup_data.user

	user_profile = UserProfile.objects.get(user=user_account)
	user_profile.is_verified = True  # Can be used for other type of verifications ie., COA id's etc,.
	user_profile.save()

	user_account.is_active = True
	user_account.save()

	signup_data.delete()  # Deleting user profile after verification of his mail.
	
	return render_to_response("login_form/confirm.html", {'confirmed':True}, context_instance=RequestContext(request))

def signin(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/home/')
	message ="" 
	if request.method == 'POST':
		print("check-1")
		form = SigninForm(request.POST)
		if form.is_valid():
#			print("check-1.1")
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
#			print("check-2")
#			return HttpResponse("Beeeep")
			user = authenticate(username=username, password=password)
				
			if user is not None:
				user_profile = UserProfile.objects.get(user=user)					
				if user.is_active and user_profile.is_verified:
					request.session['user'] = user
					login (request, user)
					if user_profile.is_new_user:
						user_profile.is_new_user = False
						user_profile.save()
					return HttpResponseRedirect("/home/")
				elif not user.is_active and not user_profile.is_verified:
					message = "Email verification is needed to access your account"
				else:
					message = "Your account has been disabled!"
			else:
				message = "Invalid username or Password!!"

	#else:
		#form = SigninForm()
	return render_to_response('frontend/landing_page/landing_page.html',{"message":message},
								 context_instance = RequestContext(request))

def signout(request):
	logout(request) # required to put a logout message here -> signin page
	msg = "You have been logged out successfully"
	return render_to_response('frontend/landing_page/landing_page.html', {'message':msg}, context_instance = RequestContext(request))
	#return HttpResponseRedirect(reverse("site_auth.views.signin"))

def upload_pic(request):
	if request.method == 'POST':
		form = UploadPicForm(request.POST, request.FILES)
		if form.is_valid():
			uprofile = UserProfile.objects.get(user = request.user)
			image = request.FILES['pic']
			filename = image.name
			ext = filename.split('.')[-1]
			image.name = uprofile.user.username +"."+ ext
			import os
			from django.conf import settings
			full_path = os.path.join(settings.MEDIA_ROOT, "profile_pics/"+image.name)
			if os.path.exists(full_path):
				os.remove(full_path)
			uprofile.image = image
			uprofile.save()
			return HttpResponseRedirect('/home/')
	else:
		form = UploadPicForm()
	return render_to_response('frontend/settings.html', {'form':form},
							context_instance = RequestContext(request))
