
from .usermanagerDAL import *
from .service import *
from utility.useful import encryption
from django.conf import settings
from .emailService import sendVerificationLink
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
logging.basicConfig(level=logging.INFO,format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',filename='../info.log', filemode='a',datefmt='%d-%b-%y %H:%M:%S')


CREDIT_POINT = 6

def reSizeImage(input_image, output_size):
    image = Image.open(input_image)
    image = ImageOps.exif_transpose(image)
    image.thumbnail(output_size)
    image_io = BytesIO()
    image.save(image_io, format='JPEG')
    resized_image = InMemoryUploadedFile(
        image_io,
        None,
        'resized_image.jpg',
        'image/jpeg',
        image_io.tell(),
        None
    )
    return resized_image

def saveUser(name,email,phone):
    if IsPhoneNumberExist(phone) :
        logging.error("Phone number Already exist")
        return False
    if IsEmailExist(email):
        logging.error("Email Already exist")
        return False
    else:
        otp = send_otp(phone)
        if otp:
            link = encryption(settings.SECRET_KEY).encrypt_string(str(phone))
            role =getRole(1)
            AddUser(name=name, phone=phone, email=email, password=otp, points=CREDIT_POINT,link=link,role=role)
            sendVerificationLink(name,[email],link) #make it async
            return True
        else:
            logging.error("Invalid Phone Number")
            return False


def updatePassword(phone):    
    if IsPhoneNumberExist(phone) :
        otp = send_otp(phone)
        if otp:
            return update_password(phone,otp)     
        else:
            return False
    else:
        return False     

   


def verifyEmail(link):
    if link != None:
       return verify_email(link)
    else:
        return False
    


