from .models import *
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from usermanager.usermanagerDAL import change_user_teacher_status
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    filename='../info.log', filemode='a', datefmt='%d-%b-%y %H:%M:%S')


def IsUserTeacher(userid):
    try:
        t = Teacher.objects.get(User_id = userid)
        return t
    except MultipleObjectsReturned:
        return True
    except ObjectDoesNotExist:
        return False
    except Exception:
        logging.info("Is teacher exist DAL")
        
        

def IsTeacherExist(teacherid):
    #This function will check is teacher id already exits of not
    try:
        return Teacher.objects.get(id = teacherid)
    except :
        return False

def IsUserTeacherExist(userid,teacherid):
    try:
        Teacher_unlock.objects.get(User_id=userid,Teacher_id = teacherid)
        logging.info("Tuition already unlocked by user")
        logging.exception(" ") 
        return True
    except ObjectDoesNotExist:
        logging.info("Tuition Not belongs to user")
        return False
    except MultipleObjectsReturned:
        logging.info("Tuition Not belongs multiple times to user")
        return True    
        


def CreateTeacher(Name, Gender, Experience, location,
                  Qualification, Subject, classes, About,
                  User_id, Teaching_mode, Phone_number,Age,Fee,Pincode):
    try:
        teacher = Teacher.objects.create(
                     Name=Name, Gender=Gender,
                     Experience=Experience, Location=location,
                     Qualification=Qualification, Subject=Subject,
                     classes=classes, About=About, User_id=User_id,
                     Teaching_mode=Teaching_mode, Phone_number=Phone_number,
                     Age=Age,Fee=Fee,Pincode=Pincode)
        change_user_teacher_status(User_id)
        teacher.save()
        return True
    except Exception:
        logging.exception("Create teacher Teacher DAL")
        return False
    
def UnlockTeacher(user,teacher):
    try:
        Teacher_unlock.objects.create(Teacher_id = teacher,User_id = user)
        return True
    except Exception:
        logging.exception("Unlock taecher DAL")
        return False

def getLatestTeacher():
    try:
        t = Teacher.objects.all().order_by('-Join_date')[:100]
        return t
    except Exception:
           logging.exception("Create teacher Teacher DAL") 
           return None    
    

def getMyTeacher(userId):
    try:
        t= Teacher_unlock.objects.filter(User_id=userId)
        return t
    except Exception:
        logging.exception("Create teacher Teacher DAL") 
        return None
            

def getTeacherInfo(userId):
    try:
        t= Teacher.objects.get(User_id=userId)
        return t
    except:
        return None


