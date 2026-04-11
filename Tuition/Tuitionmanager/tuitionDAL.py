from .models import *
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q
from django.core.paginator import Paginator

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')



#add new tuition in database
def addTuition(posted_date, user, student_name, phone_number, 
               course, subject, description, teaching_mode, fee, 
               locality,slug, photo,pincode=None,):
    
    t = Tuitions.objects.create(
            posted_date=posted_date, user_id=user, student_name=student_name, phone_number=phone_number,course=course,subject=subject,description=description,teaching_mode=teaching_mode,fee=fee,pincode=pincode,locality=locality,slug=slug,photo=photo)
    print(t.id)
    return t.id


def updateSlug(tuition_id, slug):
    Tuitions.objects.filter(id=tuition_id).update(slug=slug)


def getLatestTuition(pageNumber):
    try:  
        tuitions =  Tuitions.objects.filter(status=True).order_by('-posted_date','-id')
        paginator = Paginator(tuitions, 10)
        t = paginator.get_page(pageNumber)
        if  pageNumber > paginator.num_pages:
            return []
        return t
    except Exception:
        logging.exception("getlatestTuition")
        return False

def searchTuition(query_words, pageNumber):
    if not query_words:
        return [], 0

    combined_condition = Q()
    for word in query_words[:10]:  # limit to 10 words to prevent abuse
        word_condition = (
            Q(course__icontains=word)
            | Q(subject__icontains=word)
            | Q(description__icontains=word)
            | Q(locality__icontains=word)
            | Q(pincode__District__icontains=word)
            | Q(pincode__Devision__icontains=word)
        )
        if word.isdigit():
            word_condition |= Q(pincode__Pincode__startswith=word)
        combined_condition |= word_condition

    tuitions = (
        Tuitions.objects.filter(combined_condition, status=True)
        .select_related('pincode')
        .distinct()
        .order_by('-posted_date', '-id')
    )
    paginator = Paginator(tuitions, 10)
    if pageNumber > paginator.num_pages:
        return [], paginator.num_pages
    return paginator.get_page(pageNumber), paginator.num_pages


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
    tuition_unlocks = Tuition_unlock.objects.filter(User_id=userid)
    tuition_ids = tuition_unlocks.values_list('Tuition_id', flat=True)
    tuitions = Tuitions.objects.filter(id__in=tuition_ids) 
    return tuitions
            
def MyPost(userId):
    tuition_unlocks = Tuitions.objects.filter(user_id=userId)
    return tuition_unlocks

