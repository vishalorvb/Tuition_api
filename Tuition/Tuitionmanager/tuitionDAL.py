from .models import *
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    filename='../info.log', filemode='a', datefmt='%d-%b-%y %H:%M:%S')


def addTuition(posted_date, user, student_name, phone_number, course, subject, description, teaching_mode, fee,  locality, pincode=None,):
    try:
        new_tuition = Tuitions.objects.create(
            posted_date=posted_date, user_id=user, student_name=student_name, phone_number=phone_number,course=course,subject=subject,description=description,teaching_mode=teaching_mode,fee=fee,pincode=pincode,locality=locality)
        return True
    except Exception:
        logging.exception("add tuition in tuition DAL")
        return False

def getLatestTuition():
    try:  
        t = Tuitions.objects.filter(status = True).order_by('-posted_date')[:10]
        return t
    except Exception:
        logging.exception("getlatestTuition")
        return False
        
def getAllTuition():
    try:
        t = Tuitions.objects.filter(status = True).order_by('-posted_date')[:100]
        return t
    except Exception:
        logging.exception("getlatestTuition")   
        return False
        
def IsTuitionIdExist(id):
    try:
        t = Tuitions.objects.get(id = id)
        logging.info("Tuition id Exits")
        return t
    except Exception:
        return False
            
def unlockTuition(user,tuition):
    try:
        return Tuition_unlock.objects.create(User_id =user,Tuition_id = tuition)
    except Exception:
        return False
        
def IstuitionUserExist(userid,tutid):
    try:
        Tuition_unlock.objects.get(User_id=userid,Tuition_id = tutid)
        logging.info("Tuition already unlocked by user")
        logging.exception(" ") 
        return True
    except ObjectDoesNotExist:
        logging.info("Tuition Not belongs to user")
        return False
    except MultipleObjectsReturned:
        logging.info("Tuition Not belongs multiple times to user")
        return True
    
def changeStatus(tutionid):
    try:
        T = Tuitions.objects.get(id= tutionid)
        if T.status:
            T.status = False
            T.save()
            return True
        else:
            T.status = True
            T.save()
            return True
        
    except Exception:
        logging.exception(" ")
        return False
    
def IsTuitionBelongsToUser(userid,tuitionid):
    try:
        Tuitions.objects.filter(id=tuitionid,user_id=userid)
        return True
    except Exception:
        logging.exception(" ")
        return False
                 
def MyTuition(userid):
    try:
        return Tuitions.objects.filter(user_id=userid)                             
    except Exception:
        logging.exception(" ")
        return None
    
def Myunlocks(userid):
    try:
        t = Tuition_unlock.objects.filter(User_id=userid)
        return t
    except:
        return None    
        

