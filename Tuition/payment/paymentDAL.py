from .models import *
import logging
from django.core.exceptions import ObjectDoesNotExist
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

logger = logging.getLogger(__name__)



def CreateOrder(user, order_id, amount, plan):
    logger.info("CreateOrder: Saving order to DB orderId=%s userId=%s", order_id, user.id)
    try:
        orders.objects.create(User_id=user, Razor_Order_id=order_id,
                              amount=amount, plan=plan)
        logger.info("CreateOrder: Order saved successfully orderId=%s", order_id)
        return True
    except Exception:
        logger.exception("CreateOrder: Failed to save order orderId=%s", order_id)
        return False
    
    
def IsPlanExists(plancode):
    try:
        logger.info("IsPlanExists: Checking plancode=%s", plancode)
        p = plan.objects.get(plan_code=plancode)
        logger.info("IsPlanExists: Plan found plancode=%s", plancode)
        return p
    except:
        logger.warning("IsPlanExists: Plan not found plancode=%s", plancode)
        return False
  
def getOrderByRazorId(order_id):
    try:
        logger.info("getOrderByRazorId: Fetching orderId=%s", order_id)
        temp = orders.objects.get(Razor_Order_id=order_id)
        logger.info("getOrderByRazorId: Order found orderId=%s", order_id)
        return temp
    except Exception:
        logger.exception("getOrderByRazorId: Order not found orderId=%s", order_id)
        return False
    
def getPlans():
    logger.info("getPlans: Fetching all plans")
    return plan.objects.all()    