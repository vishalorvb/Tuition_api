from django.urls import include, path,re_path
from Tuitionmanager import views
app_name = 'tuition'
urlpatterns = [
    re_path(r'^/createTuition$', views.createTuition, name='createTuition'),
    re_path(r'^/changeStatus', views.changeStatus, name='changeStatus'),
    re_path(r'^/unlockTuition', views.unlockTuition, name='unlockTuition'),
    path('/getTuitionByid/<int:tuitionId>', views.get_tution_byId, name='tuitionByid'),
    re_path(r'^/getLatesttuition', views.getLatestTuition, name='getLatestTuition'),




    #using re_path 
    #re_path(r'^/getTuitionByid/(?P<tuitionId>\d+)/$', views.get_tution_byId, name='tuitionByid'),




]
