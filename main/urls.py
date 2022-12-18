from django.urls import path
from register import views as v
from .views import ChangePasswordView
from . import views
from two_factor import views as tviews

urlpatterns = [
    path("", tviews.LoginView.as_view(), name="login"),
    path("upload/", views.upload, name="upload"),
    path("myFiles/", views.myFiles, name="myFiles"),
    path("apfiles/", views.apfiles, name="apfiles"),
    path("resources/", views.resources, name="resources"),
    path("profile/", views.profile, name="profile"),
    path('<int:id>',views.fileinfopage , name='fileinfos'),
    path('changepass/', ChangePasswordView.as_view(), name='changepass'),
    path('search/', views.search, name='search'),
    path('filter/<str:category>', views.filter, name='filter'),
    path('userfile/<str:username>', views.userfile, name='userfile'),
    path('apfilter/<str:category>', views.apfilter, name='apfilter'),
    path('myfilter/<str:category>', views.myfilter, name='myfilter'),
]