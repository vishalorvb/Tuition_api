from .tuitionDAL import *
from django.utils import timezone
from Home.HomeDAL import isPincode
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

logger = logging.getLogger(__name__)


def saveTuition(user, student_name, phone_number, course, subject, description, photo, teaching_mode, fee, pincode=None, locality=''):
    try:
        logger.info("saveTuition: Creating tuition for userId=%s, course=%s", user.id, course)
        slug = pincode.Devision + pincode.District
        slug = slug + '-' + course.split()[0] + '-' + subject.split()[0] + '-' + locality.split()[0]
        posted_date = timezone.now()
        logger.info("saveTuition: Generated slug=%s, calling addTuition", slug)
        tuition_id = addTuition(posted_date, user, student_name, phone_number, course, subject, description, teaching_mode, fee, locality, slug, photo, pincode)
        if tuition_id:
            slug = slug + '-' + str(tuition_id)
            updateSlug(tuition_id, slug)
            logger.info("saveTuition: Tuition created tuitionId=%s", tuition_id)
        return tuition_id
    except Exception:
        logger.exception("saveTuition: Failed to save tuition for userId=%s", user.id)
        return False



def get_latest_tuition(pageNumber):
    logger.info("get_latest_tuition: Fetching page=%s", pageNumber)
    return getLatestTuition(pageNumber)



def search_tuitions(words, pageNumber):
    logger.info("search_tuitions: Searching words=%s page=%s", words, pageNumber)
    query_words = [w for w in words if len(w) >= 2]
    if not query_words:
        logger.warning("search_tuitions: No valid query words")
        return [], 0
    return searchTuition(query_words, pageNumber)



def getTution_deatils(tuitionId):
    logger.info("getTution_deatils: Fetching tuitionId=%s", tuitionId)
    return getDetails(tuitionId)


def canPhoneNumber(tuitionId, userId):
    logger.info("canPhoneNumber: Checking access tuitionId=%s userId=%s", tuitionId, userId)
    if IstuitionUserExist(userId, tuitionId) or IsTuitionBelongsToUser(userId, tuitionId):
        logger.info("canPhoneNumber: Access granted")
        return True
    logger.info("canPhoneNumber: Access denied")
    return False

def unlock_tuitions(user, tutionId):
    logger.info("unlock_tuitions: userId=%s unlocking tuitionId=%s", user.id, tutionId)
    tution = is_tutionid_exists(tutionId)
    if IstuitionUserExist(user.id, tution.id) == False and user.id != tution.user_id.id:
        if user.credit_points > 0 and unlockTuition(user, tution):
            unlock = tution.unlocks
            tution.unlocks = unlock + 1
            tution.save()
            logger.info("unlock_tuitions: Tuition unlocked successfully tuitionId=%s", tutionId)
            return tution.phone_number
        else:
            logger.warning("unlock_tuitions: Insufficient credits or unlock failed userId=%s", user.id)
            return False
    else:
        logger.info("unlock_tuitions: Already unlocked or own tuition userId=%s", user.id)
        return tution.phone_number
    
        

def is_tutionid_exists(id):
    logger.info("is_tutionid_exists: Checking tuitionId=%s", id)
    return IsTuitionIdExist(id)


def change_status_of_tuition(userid, tutionid):
    logger.info("change_status_of_tuition: userId=%s tuitionId=%s", userid, tutionid)
    pair = IsTuitionBelongsToUser(userid, tutionid)
    if pair:
        changeStatus(tutionid)
        logger.info("change_status_of_tuition: Status changed for tuitionId=%s", tutionid)
        return True
    else:
        logger.warning("change_status_of_tuition: Tuition does not belong to user userId=%s tuitionId=%s", userid, tutionid)
        return False
    
    
def isPincodeExists(pin):
    logger.info("isPincodeExists: Checking pin=%s", pin)
    return isPincode(pin)
        
def unlockedTuitionBAL(userId):
    logger.info("unlockedTuitionBAL: Fetching unlocked tuitions for userId=%s", userId)
    return Myunlocks(userId)

def userPost(userId):
    logger.info("userPost: Fetching posted tuitions for userId=%s", userId)
    return MyPost(userId)