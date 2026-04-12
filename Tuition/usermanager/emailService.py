from .service import send_Email
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def sendVerificationLink(name,email,link):
    logger.info("sendVerificationLink: Preparing verification email for %s", email)
    message = f'''
    Dear {name},

    Thank you for registering. Please click the link below to verify your account:
    {settings.URL}usermanager/verify_email/{link}

    Best regards,
    Home Tution
    '''
    send_Email('Account Verification',message,email)
    logger.info("sendVerificationLink: Verification email sent to %s", email)