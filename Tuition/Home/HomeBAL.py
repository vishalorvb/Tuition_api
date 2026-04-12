from Tuitionmanager.tuitionDAL import *
from Teacher.TeacherDAL import getMyTeacher
from .HomeDAL import *
import logging

logger = logging.getLogger(__name__)


def isPincodeExist(pincode):
    logger.info("isPincodeExist: Checking pincode=%s", pincode)
    if isPincode(pincode):
        logger.info("isPincodeExist: Pincode found")
        return True
    else:
        logger.warning("isPincodeExist: Pincode not found")
        return False
    
    
def getPincode(pin):
    logger.info("getPincode: Fetching pincodes starting with %s", pin)
    return getLikePincode(pin)
    