from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

gender_choices = (
	(u'M', u'Male'),
	(u'F', u'Female'),
)

year_choices = (
	(u'1', u'First'),
	(u'2', u'Second'),
	(u'3', u'Third'),
	(u'4', u'Fourth'),
	(u'5', u'Fifth'),

)

designation_choices = (
	(u'Stu', u'Student'),
	(u'Pro', u'Professional'),
)
class SignupForm(UserCreationForm):
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=20)
	email = forms.EmailField(label='Email address', max_length=75)
	designation = forms.ChoiceField(choices=designation_choices)
	gender = forms.ChoiceField(choices=gender_choices)
	dob = forms.DateField(label = 'Date of Birth', initial='1990-31-12')
	college = forms.CharField(max_length='30')
	course = forms.CharField(max_length='30')
	year = forms.ChoiceField(choices=year_choices)
	
	class Meta:
        	model = User
        	fields = ('first_name','last_name','username','email',)

class SigninForm(forms.Form):
	username = forms.CharField(max_length='30')
	password = forms.CharField(max_length='30', widget=forms.PasswordInput)
	remember_me = forms.BooleanField(required=False)

class UploadPicForm(forms.Form):
	pic = forms.ImageField()
