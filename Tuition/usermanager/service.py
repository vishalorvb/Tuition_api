from django.conf import settings
from django.core.mail import send_mail
import requests
from .models import CustomUser
import random
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    filename='../info.log', filemode='a', datefmt='%d-%b-%y %H:%M:%S')


def send_otp(phone_number):
    otp = str(random.randint(1000, 9999))
    try:
        if settings.ENVIRONMENT_NAME=='dev':
            print("OTP is", "1122")
            return "1122"
        else:
            url = f"https://2factor.in/API/V1/{settings.API_KEY}/SMS/{phone_number}/{otp}."
            requests.get(url)
        return otp
    except Exception:
        logging.error("OTP is not Sent")
        logging.exception("Error in otp service")
        return False


def send_Email(subject, message, receiver_list):
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, receiver_list,fail_silently=True,)
