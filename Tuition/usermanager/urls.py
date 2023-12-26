from django.urls import include, path, re_path
from usermanager import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

app_name = 'usermanager'
urlpatterns = [
    re_path(r'^/createUser$', views.createUser, name='createUser'),
    re_path(r'^/updateProfile$', views.updateProfile, name='updateProfile'),
    re_path(r'^/sendOtp$', views.sendOtp, name='sendOtp'),
    re_path(r'^/login$', views.login, name='login'),
]
