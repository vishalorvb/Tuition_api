from Tuitionmanager.tuitionDAL import *
from Teacher.TeacherDAL import getMyTeacher
from .HomeDAL import *


def isPincodeExist(pincode):
    if isPincode(pincode):
        return True
    else:
        return False
    
    
def getPincode(pin):
    return getLikePincode(pin)
    