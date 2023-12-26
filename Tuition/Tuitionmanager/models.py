from django.db import models
from usermanager.models import CustomUser
from datetime import datetime 
from Home.models import pincodes

class Tuitions(models.Model):
    posted_date = models.DateField(default=datetime.now)
    user_id = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=True)
    student_name = models.CharField(max_length=20,null=True,blank=True)
    phone_number = models.CharField(max_length=14,null=True,blank=True)
    course = models.CharField(max_length=25,null=True,blank=True)
    subject = models.CharField(max_length=25,null=True,blank=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    teaching_mode = models.CharField(max_length=10)
    fee = models.CharField(max_length=10, null=True, blank=True)
    pincode = models.ForeignKey(pincodes, on_delete=models.DO_NOTHING, default=None,null=True)
    locality = models.CharField(max_length=60, null=True, blank=True)
    unlocks = models.IntegerField(null=True, blank=True,default=0)
    verify = models.BooleanField(default=False)

    def __str__(self):
        return self.student_name + self.phone_number
    
    
    
    
class Tuition_unlock(models.Model):
    unlock_date = models.DateField(default=datetime.now)
    User_id = models.ForeignKey(CustomUser, on_delete = models.CASCADE)  
    Tuition_id = models.ForeignKey(Tuitions, on_delete = models.CASCADE)    
    
    def __str__(self):
        return  self.Tuition_id.student_name
    