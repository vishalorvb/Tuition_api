from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import CharField
from .manager import *


class Role(models.Model):
    roleId = models.IntegerField()
    roleName = models.CharField(max_length=55)

    def __str__(self):
        return self.roleName

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=12 , unique=True)
    Full_name = models.CharField(max_length=55)
    email = models.EmailField(max_length=60,null=True  , blank=True)
    credit_points = models.IntegerField(default=0)
    profilepic = models.ImageField(upload_to='profilepic',default="profilepic/profilepic.png")
    is_teacher = models.BooleanField(default=False)
    is_email_varified = models.BooleanField(default=False)
    link_token = models.CharField(max_length=255,unique=True,null=True) 
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, default=None,null=True)
    username = None
    first_name = None
    last_name= None
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.Full_name

    object = CustomUserManager()
   



