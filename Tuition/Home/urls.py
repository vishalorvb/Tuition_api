from django.urls import include, path,re_path
from Home import views
app_name = 'Home'
urlpatterns=[
    re_path(r'^$',views.Home,name='Home'), 
    re_path(r'^error$',views.error,name='error'), 
    re_path(r'^profile$',views.profile,name='profile'), 
    re_path(r'^editProfile$',views.editProfile,name='editProfile'), 
    re_path(r'^pincodeexist$',views.isPincode,name='pincodeexist'), 
    re_path(r'^test$',views.test,name='test'),
    re_path(r'^getPincode$',views.getPin,name='getPin'), 
   
]