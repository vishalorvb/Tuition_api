from .TeacherDAL import *
from Home.HomeDAL import isPincode
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    filename='../info.log', filemode='a', datefmt='%d-%b-%y %H:%M:%S')



def is_user_teacher(userid):
    return IsUserTeacher(userid)
  
def is_teacher_exist(teacherid):
    return IsTeacherExist(teacherid)    

def unlock_teacherBAL(user,teacherId):
    teacher = is_teacher_exist(teacherId)
    if IsUserTeacherExist(user.id,teacher.id) == False and user.id != teacher.user_id.id and teacher is not None:
        if user.credit_points > 0 and  UnlockTeacher(user,teacher):
            cp = user.credit_points
            user.credit_points = cp -1
            user.save()
            teacher.phone_number
            return teacher.phone_number
        else:
            return None
    return True
    


def save_teacher(name, gender, experience, 
                 location, qualification, subject, classes, 
                 about, user_id, teaching_mode, 
                 phone_number,age,fee,pincode,photo=None):
    slug =pincode.Devision + pincode.District #getting distruc for slug from pincode object
    slug = slug + '-' + classes.split()[0] + '-' + subject.split()[0] + '-' + location.split()[0]


    return CreateTeacher(name=name, gender=gender,
                        experience=experience, location=location,
                        qualification=qualification, subject=subject,
                        classes=classes, about=about, user_id=user_id,
                        teaching_mode=teaching_mode, phone_number=phone_number,
                        age=age,fee=fee,pincode=pincode,photo=photo,slug=slug)

def get_latest_teacher(pageNumber):
    return getLatestTeacher(pageNumber)    


def isPincodeExists(pin):
    return  isPincode(pin)


def getTeacher(teacherId):
    return TeacherDetails(teacherId)


def getTeacheInfo(userId):
    teacher = getTeacherInfo(userId)
    return teacher

def canPhoneNumber(user,teacherId):
    teacher  = is_teacher_exist(teacherId)
    if(IsUserTeacherExist(user.id,teacherId) or teacher.user_id.id == user.id):
        return True
    return False

def search_Teacher(query_words,pageNumber):
    return searchTuition(query_words,pageNumber)

def unlockedTeacher(userId):
    return MyTeacher(userId)