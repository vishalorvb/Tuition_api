from django.conf import settings
from django.core.mail import send_mail
import requests
from .models import CustomUser
import random
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

logger = logging.getLogger(__name__)


def send_otp(phone_number):
    logger.info("send_otp: Generating OTP for phone=%s", phone_number)
    otp = str(random.randint(1000, 9999))
    try:
        if settings.ENVIRONMENT_NAME != 'prod':
            logger.info("send_otp: Non-prod mode, returning static OTP for phone=%s", phone_number)
            return "1122"
        url = f"https://2factor.in/API/V1/{settings.API_KEY}/SMS/{phone_number}/{otp}/general"
        logger.info("send_otp: Calling 2factor API for phone=%s", phone_number)
        res = requests.get(url)
        if(res.status_code == 200):
            logger.info("send_otp: OTP sent successfully to phone=%s", phone_number)
            return otp
        logger.error("send_otp: 2factor API returned status=%s for phone=%s", res.status_code, phone_number)
        return False
    except Exception: 
        logger.exception("send_otp: Exception while sending OTP to phone=%s", phone_number)
        return False


def send_Email(subject, message, receiver_list):
    logger.info("send_Email: Sending email subject='%s' to %s", subject, receiver_list)
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, receiver_list,fail_silently=True,)
    logger.info("send_Email: Email sent to %s", receiver_list)
