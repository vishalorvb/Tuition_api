from .models import *
import logging
from django.core.exceptions import ObjectDoesNotExist
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    filename='../info.log', filemode='a', datefmt='%d-%b-%y %H:%M:%S')




def CreateOrder(user,order_id,amount,plan):
    logging.info("paymentDAL: requested for add created order in DB")
    try:
        orders.objects.create(User_id=user, Razor_Order_id=order_id,
                              amount=amount,plan=plan)
        logging.info("paymentDAL: Order detail added to DB, try block is OK")
        return True
    except Exception:
        logging.exception("paymentDAL exeption occure while adding order details to DB")
        return False
    
    
def IsPlanExists(plancode):
    try:
        return plan.objects.get(plan_code = plancode)
    except :
        logging.exception("paymentDAL plan code not exist")
        return False
  
def getOrderByRazorId(order_id):
    try:
        temp = orders.objects.get(Razor_Order_id = order_id)
        return temp
    except Exception:
        logging.exception("PaymentDAL: GetOrderByRazorId : razor pay order id not exit" )
        return False
    
def getPlans():
    return plan.objects.all()    