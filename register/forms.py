from ast import Pass
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
	email = forms.EmailField()
	first_name = forms.CharField()
	last_name = forms.CharField()

	class Meta:
		model=User
		fields = ['username','email','password1','password2','first_name','last_name']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({'class': 'regisinput my-username-class', 'placeholder':'Username'})
		self.fields['email'].widget.attrs.update({'class': 'regisinput my-username-class', 'placeholder':'Email'})
		self.fields['password1'].widget.attrs.update({'class': 'regisinput my-password1-class', 'placeholder':'Password'})
		self.fields['password2'].widget.attrs.update({'class': 'regisinput my-password1-class', 'placeholder':'Password Confirmation'})
		self.fields['first_name'].widget.attrs.update({'class': 'regisinput my-firstname-class', 'placeholder':'Firstname'})
		self.fields['last_name'].widget.attrs.update({'class': 'regisinput my-lastname-class', 'placeholder':'Lastname'})

	


class CustomLoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({'class': 'my-username-class', 'placeholder':'Username'})
		self.fields['password'].widget.attrs.update({'class': 'my-password-class', 'placeholder':'Password'})
		


class ResetPassForm(PasswordResetForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['email'].widget.attrs.update({'class': 'my-emailclass emailinput', 'placeholder':'Email'})

class PasswordResetForm(PasswordResetForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['password'].widget.attrs.update({'class': 'my-emailclass emailinput', 'placeholder':'Email'})

