import razorpay
import logging
from .paymentDAL import *
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

logger = logging.getLogger(__name__)


razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
currency = 'INR'

def create_order(user, amount, plan):
    logger.info("create_order: Creating order for userId=%s amount=%s", user.id, amount)
    try:
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
        razorpay_order_id = razorpay_order['id']
        logger.info("create_order: Razorpay order created orderId=%s", razorpay_order_id)
    except Exception:
        logger.exception("create_order: Failed to create Razorpay order for userId=%s", user.id)
        return False

    temp = CreateOrder(user, razorpay_order_id, amount, plan)
    if temp:
        context = {}
        context['order_id'] = razorpay_order_id
        context['key'] = settings.RAZOR_KEY_ID
        context['amount'] = amount
        context['currency'] = currency
        context['name'] = "Vishal store"
        logger.info("create_order: Order saved to DB orderId=%s", razorpay_order_id)
        return context
    else:
        logger.error("create_order: Failed to save order to DB orderId=%s", razorpay_order_id)
        return False

def is_plan_exist(plan_code):
    logger.info("is_plan_exist: Checking plan_code=%s", plan_code)
    return IsPlanExists(plan_code)

def verify_paymentBAL(params_dict):
    logger.info("verify_paymentBAL: Verifying payment orderId=%s", params_dict["razorpay_order_id"])
    order = getOrderByRazorId(params_dict["razorpay_order_id"])
    if order == False:
        logger.error("verify_paymentBAL: Order not found orderId=%s", params_dict["razorpay_order_id"])
        return False
        
    result = razorpay_client.utility.verify_payment_signature(
                params_dict) 
    if result:
        order.status = "Authorized" 
        order.save()
        logger.info("verify_paymentBAL: Payment signature verified, status=Authorized orderId=%s", params_dict["razorpay_order_id"])
        try:
            razorpay_client.payment.capture(params_dict["razorpay_payment_id"], order.amount)
            logger.info("verify_paymentBAL: Payment captured paymentId=%s", params_dict["razorpay_payment_id"])
            
            p = order.User_id.credit_points
            p = p + order.plan.points
            order.User_id.credit_points = p
            order.User_id.save()
            logger.info("verify_paymentBAL: Credit points updated for userId=%s, new_points=%s", order.User_id.id, p)
            return True   
        except Exception:
            logger.exception("verify_paymentBAL: Failed to capture payment paymentId=%s", params_dict["razorpay_payment_id"])
            return False 
    else:
        logger.error("verify_paymentBAL: Invalid payment signature orderId=%s", params_dict["razorpay_order_id"])
        return False
    
    
def get_plan():
    logger.info("get_plan: Fetching all plans")
    return getPlans() 