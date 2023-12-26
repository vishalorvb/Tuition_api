import razorpay
import logging
from .paymentDAL import *
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    filename='../info.log', filemode='a', datefmt='%d-%b-%y %H:%M:%S')


razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
currency = 'INR'

def create_order(user,amount,plan):
    logging.info("paymentBAL create order: requested for create a order")
    try:
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
        razorpay_order_id = razorpay_order['id']
        logging.info("paymentBAL create order: Order Created succesfully orderID: ",razorpay_order_id)
    except Exception:
        logging.exception("paymentBAL create order: Exeption occured while creating order")
        return False

    temp = CreateOrder(user,razorpay_order_id,amount,plan)
    if temp:
        context = {}
        context['order_id'] = razorpay_order_id
        context['key'] = settings.RAZOR_KEY_ID
        context['amount'] = amount
        context['currency'] = currency
        context['name'] = "Vishal store"
        return context
    else:
        return False

def is_plan_exist(plan_code):
    return IsPlanExists(plan_code)    

def verify_paymentBAL(params_dict):
    order = getOrderByRazorId(params_dict["razorpay_order_id"])
    if order ==  False:
        logging.info("paymentBAL: verify_paymentBAL: order not exist")
        return False
        
    result = razorpay_client.utility.verify_payment_signature(
                params_dict) 
    if result:
        order.status = "Authorized" 
        order.save()
        logging.info("paymentBAL: verify_paymentBAL: payment signature verified and update to Authorized")
        try:
            # capture the payemt
            razorpay_client.payment.capture(params_dict["razorpay_payment_id"], order.amount)
            logging.info("paymentBAL: verify_paymentBAL: Payment Captured succesfully")
            
            p = order.User_id.credit_points
            p = p + order.plan.points
            order.User_id.credit_points = p
            order.User_id.save()
            logging.info("paymentBAL: verify_paymentBAL: Credit point update succesfully")
            return True   
        except Exception:
            logging.exception("paymentBAL: error in capturing payment") 
            return False 
    else:
        logging.info("payment signature in not valid") 
        return False   
    
    
def get_plan():
    return getPlans() 