from django.db import models
from usermanager.models import CustomUser
from datetime import datetime 
from Home.models import pincodes


class Teacher(models.Model):
    join_date = models.DateField(default=datetime.now)
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    experience = models.IntegerField()
    location = models.CharField(max_length=50, null=True, blank=True)
    qualification = models.CharField(max_length=50)
    subject = models.CharField(max_length=20)
    classes = models.CharField(max_length=30)
    about = models.CharField(max_length=300)
    #User_id = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    user_id = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING, unique=True)
    status = models.BooleanField(default=False)
    teaching_mode = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=12)
    pincode = models.ForeignKey(pincodes, on_delete=models.DO_NOTHING, null=True,default=None)
    age = models.IntegerField(default=0)
    fee = models.CharField(max_length=5, default=0)
    photo = models.ImageField(upload_to = 'teacherphotos/',null=True)

    def __str__(self):
        return self.Name


class Teacher_unlock(models.Model):
    Teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    User_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    unlock_date = models.DateField(default=datetime.now)
    
    def __str__(self):
        return self.Teacher_id.Name