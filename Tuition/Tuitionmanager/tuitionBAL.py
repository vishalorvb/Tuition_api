from .tuitionDAL import *
from datetime import date
from Home.HomeDAL import isPincode
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    filename='../info.log', filemode='a', datefmt='%d-%b-%y %H:%M:%S')


def saveTuition(user, student_name, phone_number, course, subject, description, teaching_mode, fee, pincode=None, locality= ''):
    try:
        posted_date = date.today()
        return addTuition(posted_date, user, student_name, phone_number, course, subject, description, teaching_mode, fee,locality, pincode)
    except Exception:
        logging.exception("saveTuition in tuitionBAL")
        return False



def get_latest_tuition():
    # return first 10 tuitions only
    return getLatestTuition()

def get_all_tuition():
    return getAllTuition()

def unlock_tuitions(user,tutionId):
    tution = is_tutionid_exists(tutionId)
    if  IstuitionUserExist(user.id,tution.id) == False and user.id != tution.user_id.id :
        if user.credit_points > 0 and unlockTuition(user,tution):  
           cp = user.credit_points
           user.credit_points = cp -1
           user.save()
           unlock  = tution.unlocks
           tution.unlocks = unlock + 1
           tution.save()
           return tution.phone_number
        else:
           return False  
    else:
        return tution.phone_number
    
        

def is_tutionid_exists(id):
    return IsTuitionIdExist(id)


def change_status_of_tuition(userid,tutionid):
    pair = IsTuitionBelongsToUser(userid,tutionid)
    if pair:
        changeStatus(tutionid)
        return True
    else:
        return False
    
    
def isPincodeExists(pin):
    return  isPincode(pin)    
        
