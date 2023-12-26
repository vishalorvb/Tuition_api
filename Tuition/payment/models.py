from django.db import models
from usermanager.models import CustomUser
from datetime import datetime 


class plan(models.Model):
    plan_name = models.CharField(max_length = 50)
    plan_description = models.CharField(max_length = 200)
    price = models.IntegerField()
    plan_code = models.CharField(max_length = 20,unique=True)
    points = models.IntegerField() 
    
    def __str__(self):
        return self.plan_name


class orders(models.Model):
    Date = models.DateField(default=datetime.now)
    User_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Razor_Order_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default="Created")
    Credited = models.BooleanField(default=False)
    amount = models.IntegerField()
    plan = models.ForeignKey(plan, on_delete=models.SET_NULL,null=True)
    
    
    

        
