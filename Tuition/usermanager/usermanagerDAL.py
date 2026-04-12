from .models import *
import logging
from django.core.exceptions import ObjectDoesNotExist
logging.basicConfig(level=logging.INFO,format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',datefmt='%d-%b-%y %H:%M:%S')

logger = logging.getLogger(__name__)

def getRole(roleId):
    try:
        logger.info("getRole: Fetching role for roleId=%s", roleId)
        role = Role.objects.get(roleId=roleId)
        logger.info("getRole: Role found - %s", role)
        return role
    except:
        logger.error("getRole: Role not found for roleId=%s", roleId)
        return None
    

def IsPhoneNumberExist(phoneNumber):
    exists = CustomUser.object.filter(phone_number=phoneNumber).exists()
    logger.info("IsPhoneNumberExist: phone=%s, exists=%s", phoneNumber, exists)
    return exists


def IsEmailExist(email):
    exists = CustomUser.object.filter(email=email).exists()
    logger.info("IsEmailExist: email=%s, exists=%s", email, exists)
    return exists


def AddUser(name, email, password, phone, points, link, role):
    try:
        logger.info("AddUser: Creating user phone=%s, email=%s", phone, email)
        CustomUser.object.create_user(
            Full_name=name,
            phone_number=phone,
            email=email,
            password=password,
            credit_points=points,
            link_token=link,
            role=role,
        )
        logger.info("AddUser: User created successfully phone=%s", phone)
    except Exception:
        logger.exception("AddUser: Failed to create user phone=%s", phone)
        raise
        
        
def update_password(phone, password):
    try:
        logger.info("update_password: Updating password for phone=%s", phone)
        user = CustomUser.object.get(phone_number=phone)
        user.set_password(password)
        user.save(update_fields=['password'])
        logger.info("update_password: Password updated successfully for phone=%s", phone)
        return True
    except ObjectDoesNotExist:
        logger.error("update_password: User not found for phone=%s", phone)
        return False
    except Exception:
        logger.exception("update_password: Failed to update password for phone=%s", phone)
        return False
       
def get_user(id):
    try:
        logger.info("get_user: Fetching user for id=%s", id)
        user = CustomUser.object.get(id = id)
        logger.info("get_user: User found for id=%s", id)
        return user
    except Exception:
        logger.exception("get_user: Failed to fetch user for id=%s", id)
        return False
 
    
def get_user_bylink(link):
    try:
        logger.info("get_user_bylink: Fetching user by link_token")
        user = CustomUser.object.get(link_token = link)
        logger.info("get_user_bylink: User found")
        return user
    except:
        logger.warning("get_user_bylink: User not found for given link")
        return False
    
# def is_email_verified(link):
#     user = get_user_bylink(link)
    
             
         
def save_email_link(userId,link):
    logger.info("save_email_link: Saving link for userId=%s", userId)
    user = get_user(userId)
    if user:
        user.link_token = link
        user.save()
        logger.info("save_email_link: Link saved for userId=%s", userId)
        return True
    else:
        logger.error("save_email_link: User not found for userId=%s", userId)
        return False         


    
def verify_email(token):
    try:
        logger.info("verify_email: Verifying email for token")
        user = CustomUser.object.get(link_token = token)
        user.is_email_varified = True
        user.save()
        logger.info("verify_email: Email verified for userId=%s", user.id)
        return True
    except:
        logger.error("verify_email: Verification failed - token not found")
        return False
    


def change_user_teacher_status(userId):
        logger.info("change_user_teacher_status: Updating teacher status for userId=%s", userId)
        user = CustomUser.object.get(id = userId)
        user.is_teacher = True
        user.save()
        logger.info("change_user_teacher_status: Teacher status updated for userId=%s", userId)
        return True
 

def getUserinfo(userId):
    try:
        user = CustomUser.objects.get(id=userId) 
        return user  
    except ObjectDoesNotExist:
        logging.exception("user does not exist")
        return None
        
    
    