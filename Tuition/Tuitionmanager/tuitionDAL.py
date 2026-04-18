from .models import *
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q, Value, FloatField
from django.db.models.functions import Greatest
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator
from Home.models import pincodes

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

logger = logging.getLogger(__name__)


def addTuition(posted_date, user, student_name, phone_number, 
               course, subject, description, teaching_mode, fee, 
               locality, slug, photo, pincode=None,):
    logger.info("addTuition: Creating tuition for userId=%s, course=%s", user.id, course)
    t = Tuitions.objects.create(
            posted_date=posted_date, user_id=user, student_name=student_name, phone_number=phone_number, course=course, subject=subject, description=description, teaching_mode=teaching_mode, fee=fee, pincode=pincode, locality=locality, slug=slug, photo=photo)
    logger.info("addTuition: Tuition created tuitionId=%s", t.id)
    return t.id


def updateSlug(tuition_id, slug):
    logger.info("updateSlug: Updating slug for tuitionId=%s", tuition_id)
    Tuitions.objects.filter(id=tuition_id).update(slug=slug)


def getLatestTuition(pageNumber):
    try:
        logger.info("getLatestTuition: Fetching page=%s", pageNumber)
        tuitions = Tuitions.objects.filter(status=True).order_by('-posted_date', '-id')
        paginator = Paginator(tuitions, 20)
        t = paginator.get_page(pageNumber)
        if pageNumber > paginator.num_pages:
            logger.warning("getLatestTuition: Page %s exceeds total %s", pageNumber, paginator.num_pages)
            return []
        logger.info("getLatestTuition: Returning page %s of %s", pageNumber, paginator.num_pages)
        return t
    except Exception:
        logger.exception("getLatestTuition: Failed to fetch tuitions")
        return False

def searchTuition(query_keywords, location_keywords, pageNumber):
    logger.info("searchTuition: query=%s location=%s page=%s", query_keywords, location_keywords, pageNumber)
    if not query_keywords and not location_keywords:
        return [], 0


    # --- Step 1: Build Q objects for all keywords (OR logic for any word match) ---
    tuition_q = Q(status=True)
    trigram_exprs = []
    or_q = Q()

    # For query keywords (subject, course, locality)
    if query_keywords:
        for word in query_keywords:
            trigram_exprs.append(TrigramSimilarity('subject', word))
            trigram_exprs.append(TrigramSimilarity('course', word))
            trigram_exprs.append(TrigramSimilarity('locality', word))
            or_q |= Q(subject__icontains=word)
            or_q |= Q(course__icontains=word)
            or_q |= Q(locality__icontains=word)

    # For location keywords (locality field only)
    if location_keywords:
        for word in location_keywords:
            trigram_exprs.append(TrigramSimilarity('locality', word))
            or_q |= Q(locality__icontains=word)

    # If no keywords, return empty
    if not trigram_exprs and not or_q:
        return [], 0


    from django.db.models import F
    # Trigram similarity queryset
    trigram_qs = Tuitions.objects.filter(tuition_q).annotate(
        sim=Greatest(*trigram_exprs, output_field=FloatField())
    ).filter(sim__gte=0.2) if trigram_exprs else Tuitions.objects.none()

    # OR Q fallback queryset (any word matches any field)
    or_fallback_qs = Tuitions.objects.filter(tuition_q & or_q) if or_q else Tuitions.objects.none()

    # Combine both querysets and remove duplicates
    tuition_qs = (trigram_qs | or_fallback_qs).distinct()

    # --- Step 3: If location keywords, boost tuitions with matching pincodes ---
    pincode_scores = {}
    if location_keywords:
        # Batch all location keywords for pincodes
        pincode_q = Q()
        for word in location_keywords:
            pincode_q |= Q(District__icontains=word) | Q(Devision__icontains=word) | Q(State__icontains=word) | Q(Taluk__icontains=word) | Q(Region__icontains=word)
        matched_pincodes = pincodes.objects.filter(pincode_q).values_list('Pincode', flat=True)
        # Optionally, you can also use trigram similarity for pincodes if needed
        # But for speed, icontains is faster
        tuition_qs = tuition_qs.annotate(
            pincode_match=Q(pincode__Pincode__in=list(matched_pincodes))
        )

    # --- Step 4: Sort by similarity and posted_date ---
    tuition_qs = tuition_qs.order_by('-sim', '-posted_date', '-id')

    # --- Step 5: Paginate ---
    page_size = 20
    paginator = Paginator(tuition_qs, page_size)
    page = paginator.get_page(pageNumber)
    logger.info("searchTuition: Returning page %s of %s, total=%s", pageNumber, paginator.num_pages, paginator.count)
    return list(page), paginator.num_pages


def getDetails(tuitionId):
    try:
        logger.info("getDetails: Fetching tuitionId=%s", tuitionId)
        t = Tuitions.objects.get(id=tuitionId)
        logger.info("getDetails: Found tuitionId=%s", tuitionId)
        return t
    except ObjectDoesNotExist:
        logger.warning("getDetails: Not found tuitionId=%s", tuitionId)
        return None
    

        

def IsTuitionIdExist(id):
    try:
        logger.info("IsTuitionIdExist: Checking tuitionId=%s", id)
        t = Tuitions.objects.get(id = id)
        logger.info("IsTuitionIdExist: Found tuitionId=%s", id)
        return t
    except Exception:
        logger.warning("IsTuitionIdExist: Not found tuitionId=%s", id)
        return False
            
def unlockTuition(user, tuition):
    try:
        logger.info("unlockTuition: Unlocking tuitionId=%s for userId=%s", tuition.id, user.id)
        Tuition_unlock.objects.create(User_id=user, Tuition_id=tuition)
        logger.info("unlockTuition: Successfully unlocked")
        return True
    except Exception:
        logger.exception("unlockTuition: Failed to unlock")
        return False
        



# This will return True if user(userId) already unlocked the tuition (tuitionId)
def IstuitionUserExist(userid, tutid):
    try:
        logger.info("IstuitionUserExist: Checking userId=%s tuitionId=%s", userid, tutid)
        Tuition_unlock.objects.get(User_id=userid, Tuition_id=tutid)
        logger.info("IstuitionUserExist: Already unlocked userId=%s tuitionId=%s", userid, tutid)
        return True
    except ObjectDoesNotExist:
        logger.info("IstuitionUserExist: Not unlocked userId=%s tuitionId=%s", userid, tutid)
        return False
    except MultipleObjectsReturned:
        logger.warning("IstuitionUserExist: Multiple records userId=%s tuitionId=%s", userid, tutid)
        return True
    

def IsTuitionBelongsToUser(userid, tuitionid):
    try:
        logger.info("IsTuitionBelongsToUser: Checking userId=%s tuitionId=%s", userid, tuitionid)
        Tuitions.objects.get(id=tuitionid, user_id=userid)
        logger.info("IsTuitionBelongsToUser: Tuition belongs to user")
        return True
    except ObjectDoesNotExist:
        logger.info("IsTuitionBelongsToUser: Tuition does not belong to userId=%s", userid)
        return False



  



def changeStatus(tutionid):
    try:
        logger.info("changeStatus: Toggling status for tuitionId=%s", tutionid)
        T = Tuitions.objects.get(id=tutionid)
        if T.status:
            T.status = False
            T.save()
            logger.info("changeStatus: Status set to inactive for tuitionId=%s", tutionid)
            return True
        else:
            T.status = True
            T.save()
            logger.info("changeStatus: Status set to active for tuitionId=%s", tutionid)
            return True
        
    except Exception:
        logger.exception("changeStatus: Failed for tuitionId=%s", tutionid)
        return False
    

def MyTuition(userid):
    try:
        logger.info("MyTuition: Fetching tuitions for userId=%s", userid)
        return Tuitions.objects.filter(user_id=userid)
    except Exception:
        logger.exception("MyTuition: Failed for userId=%s", userid)
        return None
    
def Myunlocks(userid):
    logger.info("Myunlocks: Fetching unlocked tuitions for userId=%s", userid)
    tuition_unlocks = Tuition_unlock.objects.filter(User_id=userid)
    tuition_ids = tuition_unlocks.values_list('Tuition_id', flat=True)
    tuitions = Tuitions.objects.filter(id__in=tuition_ids)
    logger.info("Myunlocks: Found %s unlocked tuitions", len(tuitions))
    return tuitions
            
def MyPost(userId):
    logger.info("MyPost: Fetching posted tuitions for userId=%s", userId)
    tuition_unlocks = Tuitions.objects.filter(user_id=userId)
    logger.info("MyPost: Found %s posted tuitions", len(tuition_unlocks))
    return tuition_unlocks

