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
        paginator = Paginator(tuitions, 10)
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

    # Step 1: Search location keywords against pincode fields only
    pincode_scores = {}
    if location_keywords:
        for word in location_keywords:
            pincode_hits = pincodes.objects.annotate(
                sim=Greatest(
                    TrigramSimilarity('District', word),
                    TrigramSimilarity('Devision', word),
                    TrigramSimilarity('State', word),
                    TrigramSimilarity('Taluk', word),
                    TrigramSimilarity('Region', word),
                    output_field=FloatField(),
                )
            ).filter(sim__gte=0.3).values_list('Pincode', 'sim')
            for pk, sim in pincode_hits:
                pincode_scores[pk] = max(pincode_scores.get(pk, 0), sim)
        logger.info("searchTuition: Matched %s pincodes", len(pincode_scores))

    # Step 2: Search query keywords against tuition fields only
    tuition_scores = {}
    if query_keywords:
        for word in query_keywords:
            tuition_hits = Tuitions.objects.filter(status=True).annotate(
                sim=Greatest(
                    TrigramSimilarity('subject', word),
                    TrigramSimilarity('course', word),
                    TrigramSimilarity('locality', word),
                    output_field=FloatField(),
                )
            ).filter(sim__gte=0.3).values_list('id', 'sim')
            for tid, sim in tuition_hits:
                tuition_scores[tid] = max(tuition_scores.get(tid, 0), sim)
        logger.info("searchTuition: Matched %s tuitions by query", len(tuition_scores))

    # Step 3: Combine results based on what params were provided
    if query_keywords and location_keywords:
        # Both provided: intersect — tuitions must match query AND be in matched pincodes
        if not pincode_scores or not tuition_scores:
            return [], 0
        pincode_tuition_ids = set(
            Tuitions.objects.filter(status=True, pincode__Pincode__in=list(pincode_scores.keys()))
            .values_list('id', flat=True)
        )
        matching_ids = set(tuition_scores.keys()) & pincode_tuition_ids
        if not matching_ids:
            return [], 0

        # Score = tuition field score + pincode score
        final_scores = {}
        pincode_map = dict(
            Tuitions.objects.filter(id__in=matching_ids)
            .values_list('id', 'pincode__Pincode')
        )
        for tid in matching_ids:
            score = tuition_scores.get(tid, 0)
            pk = pincode_map.get(tid)
            if pk and pk in pincode_scores:
                score += pincode_scores[pk]
            final_scores[tid] = score

    elif query_keywords:
        # Only query: rank by tuition field score
        final_scores = tuition_scores

    else:
        # Only location: all tuitions in matched pincodes, scored by pincode similarity
        if not pincode_scores:
            return [], 0
        pincode_tuitions = Tuitions.objects.filter(
            status=True, pincode__Pincode__in=list(pincode_scores.keys())
        ).values_list('id', 'pincode__Pincode')
        final_scores = {}
        for tid, pk in pincode_tuitions:
            final_scores[tid] = pincode_scores.get(pk, 0)

    if not final_scores:
        return [], 0

    # Step 4: Sort by relevance score descending
    sorted_ids = sorted(final_scores.keys(), key=lambda tid: final_scores[tid], reverse=True)

    # Step 5: Paginate
    page_size = 10
    total_pages = (len(sorted_ids) + page_size - 1) // page_size
    if pageNumber > total_pages:
        logger.warning("searchTuition: Page %s exceeds total %s", pageNumber, total_pages)
        return [], total_pages

    start = (pageNumber - 1) * page_size
    end = start + page_size
    page_ids = sorted_ids[start:end]

    tuitions_map = {t.id: t for t in Tuitions.objects.filter(id__in=page_ids).select_related('pincode')}
    tuitions = [tuitions_map[tid] for tid in page_ids if tid in tuitions_map]

    logger.info("searchTuition: Returning page %s of %s, total=%s", pageNumber, total_pages, len(sorted_ids))
    return tuitions, total_pages


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

