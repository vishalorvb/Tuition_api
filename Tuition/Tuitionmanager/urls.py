from django.urls import include, path,re_path
from Tuitionmanager import views
app_name = 'tuition'
urlpatterns = [
    re_path(r'^/createTuition$', views.createTuition, name='createTuition'),
    re_path(r'^/changeStatus', views.changeStatus, name='changeStatus'),
    re_path(r'^/unlockTuition', views.unlockTuition, name='unlockTuition'),



]
