from .models import *
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    filename='../info.log', filemode='a', datefmt='%d-%b-%y %H:%M:%S')



#add new tuition in database
def addTuition(posted_date, user, student_name, phone_number, course, subject, description, teaching_mode, fee,  locality,slug, pincode=None,):
    try:
        Tuitions.objects.create(
            posted_date=posted_date, user_id=user, student_name=student_name, phone_number=phone_number,course=course,subject=subject,description=description,teaching_mode=teaching_mode,fee=fee,pincode=pincode,locality=locality,slug=slug)
        return True
    except Exception:
        logging.exception("add tuition in tuition DAL")
        return False

def getLatestTuition():
    try:  
        t =  Tuitions.objects.filter(status=True).order_by('-posted_date','-id')[:10]
        return t
    except Exception:
        logging.exception("getlatestTuition")
        return False
    

def getDetails(tuitionId):
    try:
        t = Tuitions.objects.get(id=tuitionId)
        return t
    except ObjectDoesNotExist:
        return None
    

        

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
        



# This will return True if user(userId) already unlocked the tuition (tuitionId)
def IstuitionUserExist(userid,tutid):
    try:
        Tuition_unlock.objects.get(User_id=userid,Tuition_id = tutid)
        return True
    except ObjectDoesNotExist:
        logging.info("Tuition Not belongs to user")
        return False
    except MultipleObjectsReturned:
        logging.info("Tuition Not belongs multiple times to user")
        return True
    

# this will return True if tuition belogs to user, means the given tuition(tuitionId) is posted by user(userId) 
def IsTuitionBelongsToUser(userid,tuitionid):
    try:
        Tuitions.objects.get(id=tuitionid,user_id=userid)
        return True
    except ObjectDoesNotExist:
        logging.exception(" ")
        return False


def searchTuition(query_words):
    combined_condition = Q()
    for word in query_words:
        combined_condition |= Q(course__icontains=word)
        combined_condition |= Q(subject__icontains=word)
        combined_condition |= Q(locality__icontains=word)
        combined_condition |= Q(slug__icontains=word)


        combined_condition |= Q(pincode__District__contains=word)
        combined_condition |= Q(pincode__Devision__contains=word)
    tuitions = Tuitions.objects.filter(combined_condition)
    return tuitions

  



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
        

