from .models import *
import logging
logger = logging.getLogger(__name__)



def isPincode(pincode):
    try:
        pin = pincodes.objects.get(Pincode = pincode)
        return pin
    except Exception:
        return False
    
    
    
def getLikePincode(pin):
    val = pincodes.objects.filter(Pincode__startswith=pin).values('Pincode')[:10]
    return val

    



  