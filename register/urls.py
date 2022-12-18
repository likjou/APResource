from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path("", views.customLogin, name="login"),
    # path("login/", views.customLogin, name="login"),
    path("logout/", views.customLogout, name="logout"),
    path("register/", views.register, name="register"),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="registration/passwordresetdone.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="registration/passwordresetconfirm.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/passwordresetcomplete.html"), name="password_reset_complete"),

]