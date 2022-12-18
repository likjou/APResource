from django.shortcuts import render, redirect
from .forms import RegisterForm,CustomLoginForm, ResetPassForm
from django.contrib.auth import authenticate, login, logout

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


# Create your views here.

# register view

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
        
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form":form})

# login view
def customLogin(request):
    form = CustomLoginForm()
    message = ''
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            print("crdentials checked")
            if user is not None:
                login(request, user)
                return redirect("/resources")
            else:
                message = "login Failed. Please try again"
                print(message)
                return render(request,'registration/login.html',)

    return render(request,'registration/login.html',{"form":form, "message":message})

def customLogout(request):
    logout(request)
    return redirect('/account/login')


def password_reset_request(request):
    message = ''
    if request.method == "POST":
        password_reset_form = ResetPassForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.txt"
                    c = {
		            "email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'APResource',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject,email, 'wowmyemailsolong@gmail.com' , [user.email])
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/reset_password_sent")
            else:
                message = "There are no Users associated with this email. Please Try Again."
                password_reset_form = ResetPassForm()
                return render(request, 'registration/password_reset.html', {"password_reset_form":password_reset_form,"message":message})

    password_reset_form = ResetPassForm()
    return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form":password_reset_form})
