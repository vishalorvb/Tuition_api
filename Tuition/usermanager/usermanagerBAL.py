
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


CREDIT_POINT = 6



def saveUser(name, email, phone):
    if IsPhoneNumberExist(phone):
        logging.error("Phone number Already exist")
        return "Phone number Already exist"
    if IsEmailExist(email):
        logging.error("Email Already exist")
        return "Email Already exist"

    otp = send_otp(phone)
    if not otp:
        logging.error("Otp sending failed")
        return "Invalid Phone Number"

    link = encryption(settings.SECRET_KEY).encrypt_string(str(phone))
    role = getRole(1)
    AddUser(name=name, phone=phone, email=email, password=otp, points=CREDIT_POINT, link=link, role=role)
    threading.Thread(target=sendVerificationLink, args=(name, [email], link)).start()
    return None
        
def isEmailexist(email):
    return IsEmailExist(email)


def updatePassword(phone):
    if not IsPhoneNumberExist(phone):
        return False
    otp = send_otp(phone)
    if not otp:
        return False
    return update_password(phone, otp)

   


def verifyEmail(link):
    if link != None:
       return verify_email(link)
    else:
        return False
    


def getUserdata(userId):
    return getUserinfo(userId)