from django.conf.urls import url
from django.contrib import admin

# from myapis.views import UserCreateAPIView,UserLoginAPIView,UsersAPIView
from myapis.views import *

urlpatterns = [
    url(r'^api/v1/login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^api/v1/register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^api/v1/users/all$', UsersAPIView.as_view(), name='users'),
    url(r'^api/v1/user/info/(?P<pk>\d+)/$', ProfileAPIView.as_view(), name='profile'),
]
