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
    if IsUserTeacherExist(user.id,teacher.id) == False and user.id != teacher.User_id.id :
        if user.credit_points > 0 and  UnlockTeacher(user,teacher):
            cp = user.credit_points
            user.credit_points = cp -1
            user.save()
            return True
        else:
            return False
    return True
    


def save_teacher(Name, Gender, Experience, 
                 Location, Qualification, Subject, classes, 
                 About, User_id, Teaching_mode, 
                 Phone_number,Age,Fee,Pincode):
    return CreateTeacher(Name=Name, Gender=Gender,
                        Experience=Experience, location=Location,
                        Qualification=Qualification, Subject=Subject,
                        classes=classes, About=About, User_id=User_id,
                        Teaching_mode=Teaching_mode, Phone_number=Phone_number,
                        Age=Age,Fee=Fee,Pincode=Pincode)

def get_latest_teacher():
    return getLatestTeacher()    


def isPincodeExists(pin):
    return  isPincode(pin)


def getTeacher(userId):
    pass


def getTeacheInfo(userId):
    teacher = getTeacherInfo(userId)
    return teacher