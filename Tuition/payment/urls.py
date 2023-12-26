from django.urls import include, path,re_path
from payment import views
# from django.conf.urls import url

app_name = 'payment'
urlpatterns=[
    re_path('create_order',views.Create_payment_order,name='payment'),
    re_path('verify_payment',views.verify_payment,name='verify_payment'),   
    re_path('orderdetails',views.getorderdetails,name='orderdetails'),   
]
