from django.db import models
from usermanager.models import CustomUser
from datetime import datetime 
from Home.models import pincodes


class Teacher(models.Model):
    Join_date = models.DateField(default=datetime.now)
    Name = models.CharField(max_length=20)
    Gender = models.CharField(max_length=10)
    Experience = models.IntegerField()
    Location = models.CharField(max_length=50, null=True, blank=True)
    Qualification = models.CharField(max_length=50)
    Subject = models.CharField(max_length=20)
    classes = models.CharField(max_length=30)
    About = models.CharField(max_length=300)
    User_id = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    Premium = models.BooleanField(default=False)
    Teaching_mode = models.CharField(max_length=10)
    Phone_number = models.CharField(max_length=12)
    Pincode = models.ForeignKey(pincodes, on_delete=models.DO_NOTHING, null=True,default=None)
    Age = models.IntegerField(default=0)
    Fee = models.CharField(max_length=5, default=0)
    Photo = models.ImageField(upload_to = 'images/',null=True)

    def __str__(self):
        return self.Name


class Teacher_unlock(models.Model):
    Teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    User_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    unlock_date = models.DateField(default=datetime.now)
    
    def __str__(self):
        return self.Teacher_id.Name