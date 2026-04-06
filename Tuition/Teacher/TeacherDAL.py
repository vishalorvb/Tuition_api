from .models import *
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from usermanager.usermanagerDAL import change_user_teacher_status
from django.core.paginator import Paginator
from django.db.models import Q
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    filename='../info.log', filemode='a', datefmt='%d-%b-%y %H:%M:%S')


def IsUserTeacher(userid):
    try:
        t = Teacher.objects.get(user_id = userid)
        return t
    except ObjectDoesNotExist:
        logging.info("Teacher does not exist")
        return False

        
        

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
        


def CreateTeacher(name, gender, experience, location,
                  qualification, subject, classes, about,
                  user_id, teaching_mode, phone_number,age,fee,pincode,slug,photo=None):
    try:
        teacher = Teacher.objects.create(
                     name=name, gender=gender,
                     experience=experience, location=location,
                     qualification=qualification, subject=subject,
                     classes=classes, about=about, user_id=user_id,
                     teaching_mode=teaching_mode, phone_number=phone_number,
                     age=age,fee=fee,pincode=pincode,photo=photo,slug=slug)
        change_user_teacher_status(user_id.id)
        return teacher
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

def getLatestTeacher(pageNumber):
    try:
        teacher = Teacher.objects.all().order_by('-join_date','-id')
        paginator = Paginator(teacher, 10)
        t = paginator.get_page(pageNumber)
        if  pageNumber > paginator.num_pages:
            return []
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
        t= Teacher.objects.get(user_id=userId)
        return t
    except ObjectDoesNotExist:
        return None


def TeacherDetails(teacherId):
    try:
        t = Teacher.objects.get(id=teacherId)
        return t
    except ObjectDoesNotExist:
        return None


def searchTeacher(query_words, pageNumber):
    if not query_words:
        return [], 0

    combined_condition = Q()
    for word in query_words[:10]:
        word_condition = (
            Q(classes__icontains=word)
            | Q(subject__icontains=word)
            | Q(location__icontains=word)
            | Q(about__icontains=word)
            | Q(qualification__icontains=word)
            | Q(pincode__District__icontains=word)
            | Q(pincode__Devision__icontains=word)
        )
        if word.isdigit():
            word_condition |= Q(pincode__Pincode__startswith=word)
        combined_condition |= word_condition

    teachers = (
        Teacher.objects.filter(combined_condition, status=True)
        .select_related('pincode')
        .distinct()
        .order_by('-join_date', '-id')
    )
    paginator = Paginator(teachers, 10)
    if pageNumber > paginator.num_pages:
        return [], paginator.num_pages
    return paginator.get_page(pageNumber), paginator.num_pages


def MyTeacher(userId):
    teacher_unlocks = Teacher_unlock.objects.filter(User_id=userId)
    teacher_ids = teacher_unlocks.values_list('Teacher_id', flat=True)
    tuitions = Teacher.objects.filter(id__in=teacher_ids) 
    return tuitions