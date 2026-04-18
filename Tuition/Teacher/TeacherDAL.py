from .models import *
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from usermanager.usermanagerDAL import change_user_teacher_status
from django.core.paginator import Paginator
from django.db.models import Q, Value, FloatField
from django.db.models.functions import Greatest
from django.contrib.postgres.search import TrigramSimilarity
from Home.models import pincodes
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


def searchTeacher(query_keywords, location_keywords, pageNumber):
    logger.info("searchTeacher: query=%s location=%s page=%s", query_keywords, location_keywords, pageNumber)
    if not query_keywords and not location_keywords:
        return [], 0

    # Step 1: Location search — pincode fields + teacher.location (single query each)
    pincode_scores = {}
    location_teacher_scores = {}
    if location_keywords:
        # Build one annotated query for all location words against pincodes
        annotations = {}
        for i, word in enumerate(location_keywords):
            annotations[f's{i}'] = Greatest(
                TrigramSimilarity('District', word),
                TrigramSimilarity('Devision', word),
                TrigramSimilarity('State', word),
                TrigramSimilarity('Taluk', word),
                TrigramSimilarity('Region', word),
                output_field=FloatField(),
            )
        filter_q = Q()
        for key in annotations:
            filter_q |= Q(**{f'{key}__gte': 0.3})
        for row in pincodes.objects.annotate(**annotations).filter(filter_q).values_list('Pincode', *annotations.keys()):
            pk = row[0]
            best = max(row[1:])
            pincode_scores[pk] = max(pincode_scores.get(pk, 0), best)

        # Single query for teacher.location match across all words
        loc_annotations = {}
        for i, word in enumerate(location_keywords):
            loc_annotations[f'ls{i}'] = TrigramSimilarity('location', word)
        loc_filter_q = Q()
        for key in loc_annotations:
            loc_filter_q |= Q(**{f'{key}__gte': 0.3})
        for row in Teacher.objects.annotate(**loc_annotations).filter(loc_filter_q).values_list('id', *loc_annotations.keys()):
            tid = row[0]
            best = max(row[1:])
            location_teacher_scores[tid] = max(location_teacher_scores.get(tid, 0), best)

        logger.info("searchTeacher: Matched %s pincodes, %s teachers by location", len(pincode_scores), len(location_teacher_scores))

    # Step 2: Query search — teacher fields (single query for all words)
    teacher_scores = {}
    if query_keywords:
        q_annotations = {}
        for i, word in enumerate(query_keywords):
            q_annotations[f'qs{i}'] = Greatest(
                TrigramSimilarity('subject', word),
                TrigramSimilarity('classes', word),
                TrigramSimilarity('location', word),
                TrigramSimilarity('qualification', word),
                output_field=FloatField(),
            )
        q_filter = Q()
        for key in q_annotations:
            q_filter |= Q(**{f'{key}__gte': 0.3})
        for row in Teacher.objects.annotate(**q_annotations).filter(q_filter).values_list('id', *q_annotations.keys()):
            tid = row[0]
            best = max(row[1:])
            teacher_scores[tid] = max(teacher_scores.get(tid, 0), best)
        logger.info("searchTeacher: Matched %s teachers by query", len(teacher_scores))

    # Step 3: Combine results
    if query_keywords and location_keywords:
        if not pincode_scores and not location_teacher_scores:
            return [], 0
        if not teacher_scores:
            return [], 0

        pincode_teacher_map = {}
        if pincode_scores:
            for tid, pk in Teacher.objects.filter(pincode__Pincode__in=list(pincode_scores.keys())).values_list('id', 'pincode__Pincode'):
                pincode_teacher_map[tid] = pk

        location_matched_ids = set(pincode_teacher_map.keys()) | set(location_teacher_scores.keys())
        matching_ids = set(teacher_scores.keys()) & location_matched_ids
        if not matching_ids:
            return [], 0

        final_scores = {}
        for tid in matching_ids:
            score = teacher_scores.get(tid, 0)
            pk = pincode_teacher_map.get(tid)
            if pk and pk in pincode_scores:
                score += pincode_scores[pk]
            if tid in location_teacher_scores:
                score += location_teacher_scores[tid]
            final_scores[tid] = score

    elif query_keywords:
        final_scores = teacher_scores

    else:
        final_scores = {}
        if pincode_scores:
            for tid, pk in Teacher.objects.filter(pincode__Pincode__in=list(pincode_scores.keys())).values_list('id', 'pincode__Pincode'):
                final_scores[tid] = pincode_scores.get(pk, 0)
        for tid, sim in location_teacher_scores.items():
            final_scores[tid] = max(final_scores.get(tid, 0), sim)

    if not final_scores:
        return [], 0

    # Fetch join_date for sorting
    date_map = dict(Teacher.objects.filter(id__in=final_scores.keys()).values_list('id', 'join_date'))

    # Step 4: Sort by relevance score desc, then join_date desc (newest first)
    sorted_ids = sorted(final_scores.keys(), key=lambda tid: (final_scores[tid], date_map.get(tid)), reverse=True)

    # Step 5: Paginate
    page_size = 20
    total_pages = (len(sorted_ids) + page_size - 1) // page_size
    if pageNumber > total_pages:
        logger.warning("searchTeacher: Page %s exceeds total %s", pageNumber, total_pages)
        return [], total_pages

    start = (pageNumber - 1) * page_size
    end = start + page_size
    page_ids = sorted_ids[start:end]

    teachers_map = {t.id: t for t in Teacher.objects.filter(id__in=page_ids).select_related('pincode')}
    teachers = [teachers_map[tid] for tid in page_ids if tid in teachers_map]

    logger.info("searchTeacher: Returning page %s of %s, total=%s", pageNumber, total_pages, len(sorted_ids))
    return teachers, total_pages


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