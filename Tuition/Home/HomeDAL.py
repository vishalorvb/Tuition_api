from .models import *
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    filename='../info.log', filemode='a', datefmt='%d-%b-%y %H:%M:%S')



def isPincode(pincode):
    try:
        pin = pincodes.objects.get(Pincode = pincode)
        return pin
    except Exception:
        return False
    
    
    
def getLikePincode(pin):
    val = pincodes.objects.filter(Pincode__startswith=pin).values('Pincode')
    return val

    



  