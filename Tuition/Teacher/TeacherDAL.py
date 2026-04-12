from .models import *
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from usermanager.usermanagerDAL import change_user_teacher_status
from django.core.paginator import Paginator
from django.db.models import Q
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

logger = logging.getLogger(__name__)


def IsUserTeacher(userid):
    try:
        logger.info("IsUserTeacher: Checking userId=%s", userid)
        t = Teacher.objects.get(user_id = userid)
        logger.info("IsUserTeacher: Teacher found for userId=%s", userid)
        return t
    except ObjectDoesNotExist:
        logger.info("IsUserTeacher: Teacher does not exist for userId=%s", userid)
        return False

        
        

def IsTeacherExist(teacherid):
    try:
        logger.info("IsTeacherExist: Checking teacherId=%s", teacherid)
        teacher = Teacher.objects.get(id = teacherid)
        logger.info("IsTeacherExist: Teacher found teacherId=%s", teacherid)
        return teacher
    except:
        logger.warning("IsTeacherExist: Teacher not found teacherId=%s", teacherid)
        return False

def IsUserTeacherExist(userid, teacherid):
    try:
        logger.info("IsUserTeacherExist: Checking userId=%s teacherId=%s", userid, teacherid)
        Teacher_unlock.objects.get(User_id=userid, Teacher_id=teacherid)
        logger.info("IsUserTeacherExist: Already unlocked userId=%s teacherId=%s", userid, teacherid)
        return True
    except ObjectDoesNotExist:
        logger.info("IsUserTeacherExist: Not unlocked userId=%s teacherId=%s", userid, teacherid)
        return False
    except MultipleObjectsReturned:
        logger.warning("IsUserTeacherExist: Multiple unlock records userId=%s teacherId=%s", userid, teacherid)
        return True    
        


def CreateTeacher(name, gender, experience, location,
                  qualification, subject, classes, about,
                  user_id, teaching_mode, phone_number, age, fee, pincode, slug, photo=None):
    try:
        logger.info("CreateTeacher: Creating teacher name=%s for userId=%s", name, user_id.id)
        teacher = Teacher.objects.create(
                     name=name, gender=gender,
                     experience=experience, location=location,
                     qualification=qualification, subject=subject,
                     classes=classes, about=about, user_id=user_id,
                     teaching_mode=teaching_mode, phone_number=phone_number,
                     age=age, fee=fee, pincode=pincode, photo=photo, slug=slug)
        logger.info("CreateTeacher: Teacher created teacherId=%s, updating user teacher status", teacher.id)
        change_user_teacher_status(user_id.id)
        return teacher
    except Exception:
        logger.exception("CreateTeacher: Failed to create teacher")
        return False
    
def UnlockTeacher(user, teacher):
    try:
        logger.info("UnlockTeacher: Unlocking teacherId=%s for userId=%s", teacher.id, user.id)
        Teacher_unlock.objects.create(Teacher_id=teacher, User_id=user)
        logger.info("UnlockTeacher: Successfully unlocked")
        return True
    except Exception:
        logger.exception("UnlockTeacher: Failed to unlock")
        return False

def getLatestTeacher(pageNumber):
    try:
        logger.info("getLatestTeacher: Fetching page=%s", pageNumber)
        teacher = Teacher.objects.all().order_by('-join_date', '-id')
        paginator = Paginator(teacher, 10)
        t = paginator.get_page(pageNumber)
        if pageNumber > paginator.num_pages:
            logger.warning("getLatestTeacher: Page %s exceeds total pages %s", pageNumber, paginator.num_pages)
            return []
        logger.info("getLatestTeacher: Returning page %s of %s", pageNumber, paginator.num_pages)
        return t
    except Exception:
        logger.exception("getLatestTeacher: Failed to fetch teachers")
        return None    
    

def getMyTeacher(userId):
    try:
        logger.info("getMyTeacher: Fetching unlocked teachers for userId=%s", userId)
        t = Teacher_unlock.objects.filter(User_id=userId)
        return t
    except Exception:
        logger.exception("getMyTeacher: Failed for userId=%s", userId)
        return None
            

def getTeacherInfo(userId, teacherId):
    try:
        logger.info("getTeacherInfo: Fetching teacherId=%s for userId=%s", teacherId, userId)
        t = Teacher.objects.get(id=teacherId, user_id=userId)
        logger.info("getTeacherInfo: Teacher found teacherId=%s for userId=%s", teacherId, userId)
        return t
    except ObjectDoesNotExist:
        logger.warning("getTeacherInfo: Teacher not found teacherId=%s for userId=%s", teacherId, userId)
        return None


def TeacherDetails(teacherId):
    try:
        logger.info("TeacherDetails: Fetching teacherId=%s", teacherId)
        t = Teacher.objects.get(id=teacherId)
        logger.info("TeacherDetails: Found teacherId=%s", teacherId)
        return t
    except ObjectDoesNotExist:
        logger.warning("TeacherDetails: Not found teacherId=%s", teacherId)
        return None


def searchTeacher(query_words, pageNumber):
    logger.info("searchTeacher: Searching words=%s page=%s", query_words, pageNumber)
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
        logger.warning("searchTeacher: Page %s exceeds total %s", pageNumber, paginator.num_pages)
        return [], paginator.num_pages
    logger.info("searchTeacher: Found results, returning page %s of %s", pageNumber, paginator.num_pages)
    return paginator.get_page(pageNumber), paginator.num_pages


def MyTeacher(userId):
    logger.info("MyTeacher: Fetching unlocked teachers for userId=%s", userId)
    teacher_unlocks = Teacher_unlock.objects.filter(User_id=userId)
    teacher_ids = teacher_unlocks.values_list('Teacher_id', flat=True)
    tuitions = Teacher.objects.filter(id__in=teacher_ids) 
    logger.info("MyTeacher: Found %s unlocked teachers", len(tuitions))
    return tuitions

def getTeachersByUserId(user_id):
    logger.info("getTeachersByUserId: Fetching teachers for userId=%s", user_id)
    return Teacher.objects.filter(user_id=user_id)