from .models import *
import logging
logger = logging.getLogger(__name__)



def isPincode(pincode):
    try:
        logger.info("isPincode: Looking up pincode=%s", pincode)
        pin = pincodes.objects.get(Pincode = pincode)
        logger.info("isPincode: Found pincode=%s", pincode)
        return pin
    except Exception:
        logger.warning("isPincode: Pincode not found - %s", pincode)
        return False
    
    
    
def getLikePincode(pin):
    logger.info("getLikePincode: Searching pincodes starting with %s", pin)
    val = pincodes.objects.filter(Pincode__startswith=pin).values('Pincode')[:10]
    logger.info("getLikePincode: Found %s results", len(val))
    return val

    



  