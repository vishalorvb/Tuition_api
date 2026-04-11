from .models import *
import logging
from django.core.exceptions import ObjectDoesNotExist
logging.basicConfig(level=logging.INFO,format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',datefmt='%d-%b-%y %H:%M:%S')

def getRole(roleId):
    try:
        return Role.objects.get(roleId=roleId)
    except:
        return None
    

def IsPhoneNumberExist(phoneNumber):
    return CustomUser.object.filter(phone_number=phoneNumber).exists()


def IsEmailExist(email):
    return CustomUser.object.filter(email=email).exists()


def AddUser(name, email, password, phone, points, link, role):
    try:
        CustomUser.object.create_user(
            Full_name=name,
            phone_number=phone,
            email=email,
            password=password,
            credit_points=points,
            link_token=link,
            role=role,
        )
    except Exception:
        logging.exception("Failed to create user in DAL")
        raise
        
        
def update_password(phone, password):
    try:
        user = CustomUser.object.get(phone_number=phone)
        user.set_password(password)
        user.save(update_fields=['password'])
        logging.info("Password updated for %s", phone)
        return True
    except ObjectDoesNotExist:
        logging.error("User not found for phone: %s", phone)
        return False
    except Exception:
        logging.exception("Failed to update password in DAL")
        return False
       
def get_user(id):
    try:
        user = CustomUser.object.get(id = id)
        return user
    except Exception :
        logging.exception("DAL IsEmailExist")
        return False
 
    
def get_user_bylink(link):
    try:
        user = CustomUser.object.get(link_token = link)
        return user
    except :
        return False
    
# def is_email_verified(link):
#     user = get_user_bylink(link)
    
             
         
def save_email_link(userId,link):
    user = get_user(userId)
    if user:
        user.link_token = link
        user.save()
        return True
    else:
        return False         


    
def verify_email(token):
    try:
        user = CustomUser.object.get(link_token = token)
        user.is_email_varified = True
        user.save()
        return True
    except:
        return False
    


def change_user_teacher_status(userId):
        user = CustomUser.object.get(id = userId)
        user.is_teacher = True
        user.save()
        return True
 

def getUserinfo(userId):
    try:
        user = CustomUser.objects.get(id=userId) 
        return user  
    except ObjectDoesNotExist:
        logging.exception("user does not exist")
        return None
        
    
    