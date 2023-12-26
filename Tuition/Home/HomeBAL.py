from Tuitionmanager.tuitionDAL import *
from Teacher.TeacherDAL import getMyTeacher
from .HomeDAL import *

def getTuition():
    t = getLatestTuition()
    return t


def getMytuition(userid):
    return MyTuition(userid)


def getMyUnlockTuition(userid):
    return Myunlocks(userid)

def getmyteacher(userid):
    return getMyTeacher(userid)

def isPincodeExist(pincode):
    if isPincode(pincode):
        return True
    else:
        return False
    
    
def getPincode(pin):
    return getLikePincode(pin)
    