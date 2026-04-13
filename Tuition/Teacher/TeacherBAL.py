from .TeacherDAL import *
from Home.HomeDAL import isPincode
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

logger = logging.getLogger(__name__)


def is_user_teacher(userid):
    logger.info("is_user_teacher: Checking userId=%s", userid)
    return IsUserTeacher(userid)
  
def is_teacher_exist(teacherid):
    logger.info("is_teacher_exist: Checking teacherId=%s", teacherid)
    return IsTeacherExist(teacherid)

def unlock_teacherBAL(user, teacherId):
    logger.info("unlock_teacherBAL: userId=%s unlocking teacherId=%s", user.id, teacherId)
    teacher = is_teacher_exist(teacherId)
    if IsUserTeacherExist(user.id, teacher.id) == False and user.id != teacher.user_id.id and teacher is not None:
        if user.credit_points > 0 and UnlockTeacher(user, teacher):
            logger.info("unlock_teacherBAL: Teacher unlocked successfully teacherId=%s for userId=%s", teacherId, user.id)
            return teacher.phone_number
        else:
            logger.warning("unlock_teacherBAL: Insufficient credits or unlock failed userId=%s", user.id)
            return None
    logger.info("unlock_teacherBAL: Teacher already unlocked or is own profile userId=%s", user.id)
    return True
    


def save_teacher(name, gender, experience, 
                 location, qualification, subject, classes, 
                 about, user_id, teaching_mode, 
                 phone_number, age, fee, pincode, photo=None):
    logger.info("save_teacher: Creating teacher for userId=%s, name=%s", user_id.id, name)
    slug = pincode.Devision + pincode.District
    slug = slug + '-' + classes.split()[0] + '-' + subject.split()[0] + '-' + location.split()[0]
    logger.info("save_teacher: Generated slug=%s", slug)

    return CreateTeacher(name=name, gender=gender,
                        experience=experience, location=location,
                        qualification=qualification, subject=subject,
                        classes=classes, about=about, user_id=user_id,
                        teaching_mode=teaching_mode, phone_number=phone_number,
                        age=age, fee=fee, pincode=pincode, photo=photo, slug=slug)

def get_latest_teacher(pageNumber):
    logger.info("get_latest_teacher: Fetching page=%s", pageNumber)
    return getLatestTeacher(pageNumber)


def isPincodeExists(pin):
    logger.info("isPincodeExists: Checking pin=%s", pin)
    return isPincode(pin)


def getTeacher(teacherId):
    logger.info("getTeacher: Fetching teacherId=%s", teacherId)
    return TeacherDetails(teacherId)


def getTeacheInfo(userId, teacherId):
    logger.info("getTeacheInfo: Fetching teacher info for userId=%s teacherId=%s", userId, teacherId)
    teacher = getTeacherInfo(userId, teacherId)
    return teacher

def canPhoneNumber(user, teacherId):
    logger.info("canPhoneNumber: Checking access userId=%s teacherId=%s", user.id, teacherId)
    teacher = is_teacher_exist(teacherId)
    if(IsUserTeacherExist(user.id, teacherId) or teacher.user_id.id == user.id):
        logger.info("canPhoneNumber: Access granted")
        return True
    logger.info("canPhoneNumber: Access denied")
    return False

STOP_WORDS = {
    'tuition', 'tuitions', 'tution', 'tutions', 'tutorial', 'teacher', 'teachers',
    'in', 'at', 'on', 'for', 'the', 'a', 'an', 'of', 'to', 'and', 'or', 'is',
    'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do',
    'does', 'did', 'will', 'would', 'shall', 'should', 'may', 'might', 'can',
    'could', 'need', 'want', 'near', 'nearby', 'around', 'from', 'with', 'by',
    'me', 'my', 'i', 'we', 'our', 'best', 'good', 'top', 'find', 'get',
    'looking', 'search', 'home',
}


def clean_query(raw_query):
    words = raw_query.lower().split()
    return [w for w in words if w not in STOP_WORDS]


def search_Teacher(query, location, pageNumber):
    logger.info("search_Teacher: query='%s' location='%s' page=%s", query, location, pageNumber)
    query_keywords = clean_query(query) if query else []
    location_keywords = clean_query(location) if location else []
    logger.info("search_Teacher: query_keywords=%s location_keywords=%s", query_keywords, location_keywords)
    if not query_keywords and not location_keywords:
        logger.warning("search_Teacher: No valid keywords")
        return [], 0
    return searchTeacher(query_keywords, location_keywords, pageNumber)

def unlockedTeacher(userId):
    logger.info("unlockedTeacher: Fetching unlocked teachers for userId=%s", userId)
    return MyTeacher(userId)

def get_my_teacher_by_userid(user_id):
    logger.info("get_my_teacher_by_userid: Fetching profiles for userId=%s", user_id)
    return getTeachersByUserId(user_id)