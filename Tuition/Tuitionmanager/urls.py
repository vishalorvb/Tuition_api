from django.urls import include, path,re_path
from Tuitionmanager import views
app_name = 'tuition'
urlpatterns = [
    re_path(r'^/createTuition$', views.createTuition, name='createTuition'),
    re_path(r'^/changeStatus', views.changeStatus, name='changeStatus'),
    re_path(r'^/unlockTuition', views.unlockTuition, name='unlockTuition'),
    path('/getTuitionByid/<int:tuitionId>', views.get_tution_byId, name='tuitionByid'),
    path('/getLatesttuition/<int:pageNumber>', views.getLatestTuition, name='getLatestTuition'),
    path('/search/<int:pageNumber>/', views.search, name='searchTuition'),




    #using re_path 
    #re_path(r'^/getTuitionByid/(?P<tuitionId>\d+)/$', views.get_tution_byId, name='tuitionByid'),




]
