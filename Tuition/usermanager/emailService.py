from .service import send_Email
from django.conf import settings



def sendVerificationLink(name,email,link):
    message = f'''
    Dear {name},

    Thank you for registering. Please click the link below to verify your account:
    {settings.URL}usermanager/verify_email/{link}

    Best regards,
    Home Tution
    '''
    send_Email('Account Verification',message,email)