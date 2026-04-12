
from .usermanagerDAL import *
from .service import *
from utility.useful import encryption
from django.conf import settings
from .emailService import sendVerificationLink
from PIL import Image, ImageOps
from io import BytesIO
import threading
from django.core.files.uploadedfile import InMemoryUploadedFile
logging.basicConfig(level=logging.INFO,format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',datefmt='%d-%b-%y %H:%M:%S')

logger = logging.getLogger(__name__)


CREDIT_POINT = 6



def saveUser(name, email, phone):
    logger.info("saveUser: Starting registration for phone=%s, email=%s", phone, email)
    if IsPhoneNumberExist(phone):
        logger.error("saveUser: Phone number already exists - %s", phone)
        return "Phone number Already exist"
    if IsEmailExist(email):
        logger.error("saveUser: Email already exists - %s", email)
        return "Email Already exist"

    logger.info("saveUser: Sending OTP to phone=%s", phone)
    otp = send_otp(phone)
    if not otp:
        logger.error("saveUser: OTP sending failed for phone=%s", phone)
        return "Invalid Phone Number"

    logger.info("saveUser: OTP sent successfully, creating user for phone=%s", phone)
    link = encryption(settings.SECRET_KEY).encrypt_string(str(phone))
    role = getRole(1)
    AddUser(name=name, phone=phone, email=email, password=otp, points=CREDIT_POINT, link=link, role=role)
    logger.info("saveUser: User created, sending verification email to %s", email)
    threading.Thread(target=sendVerificationLink, args=(name, [email], link)).start()
    logger.info("saveUser: Registration completed for phone=%s", phone)
    return None
        
def isEmailexist(email):
    logger.info("isEmailexist: Checking email=%s", email)
    return IsEmailExist(email)


def updatePassword(phone):
    logger.info("updatePassword: Starting for phone=%s", phone)
    if not IsPhoneNumberExist(phone):
        logger.error("updatePassword: Phone number not found - %s", phone)
        return False
    logger.info("updatePassword: Phone exists, sending OTP to phone=%s", phone)
    otp = send_otp(phone)
    if not otp:
        logger.error("updatePassword: OTP sending failed for phone=%s", phone)
        return False
    logger.info("updatePassword: OTP sent, updating password for phone=%s", phone)
    return update_password(phone, otp)

   


def verifyEmail(link):
    logger.info("verifyEmail: Verifying email link")
    if link != None:
       result = verify_email(link)
       if result:
           logger.info("verifyEmail: Email verified successfully")
       else:
           logger.warning("verifyEmail: Email verification failed - invalid link")
       return result
    else:
        logger.warning("verifyEmail: Link is None")
        return False
    


def getUserdata(userId):
    logger.info("getUserdata: Fetching user data for userId=%s", userId)
    return getUserinfo(userId)