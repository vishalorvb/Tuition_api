from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render
from .paymentBAL import *
import razorpay
import logging
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from usermanager.models import CustomUser
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest,HttpResponseNotAllowed
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

logger = logging.getLogger(__name__)



def getorderdetails(request):
    if request.method == "GET":
        logger.info("getorderdetails: Request received")
        try:
            plan_code = request.GET["plan"] 
        except Exception:
            logger.exception("getorderdetails: Missing plan parameter")
            return HttpResponseRedirect(reverse('Home:error'))
        
        logger.info("getorderdetails: Checking plan_code=%s", plan_code)
        plan = is_plan_exist(plan_code)
        if plan == False:
            logger.warning("getorderdetails: Plan not found plan_code=%s", plan_code)
            return HttpResponseRedirect(reverse('Home:error'))
        
        if request.user.is_authenticated:
            logger.info("getorderdetails: Creating order for userId=%s plan=%s", request.user.id, plan_code)
            callback_url = '/payment/verify_payment'
            context = create_order(request.user, plan.price, plan)
            if context:
                context['callback_url'] = callback_url
                logger.info("getorderdetails: Order created successfully")
                return JsonResponse(context)
        else:
            logger.warning("getorderdetails: User not authenticated")
            context = {
                    "name": "none"
                } 
            request.session['redirect_url_name'] = '/payment/create_order' 
            return JsonResponse(context) 
             
    
# @login_required(login_url="/usermanager/login")
def Create_payment_order(request):
    logger.info("Create_payment_order: Rendering payment page")
    plans = get_plan()
    silver = {"price":0,"credit":0}
    gold = {"price":0,"credit":0}
    for plan in plans:
        if plan.plan_code == "1":
            silver["price"] = plan.price/100
            silver["credit"] = plan.points
        if plan.plan_code == "2":
            gold["price"] = plan.price/100
            gold["credit"] = plan.points
    context = {
        "silver":silver,
        "gold":gold
    }           
    return render(request, 'payment/payment_page.html',context)


@csrf_exempt
def verify_payment(request):
 
    if request.method == "POST":
        logger.info("verify_payment: Payment verification request received")
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            logger.info("verify_payment: Verifying orderId=%s paymentId=%s", razorpay_order_id, payment_id)
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            temp = verify_paymentBAL(params_dict)
            if temp:
                logger.info("verify_payment: Payment verified successfully orderId=%s", razorpay_order_id)
                return HttpResponseRedirect(reverse('Home:profile'))
            else:
                logger.error("verify_payment: Payment verification failed orderId=%s", razorpay_order_id)
                return HttpResponseRedirect(reverse('Home:error'))
            
           
        except:
            logger.exception("verify_payment: Missing required parameters")
            return HttpResponseBadRequest()
    else:
        logger.warning("verify_payment: Non-POST request received")
        return HttpResponseBadRequest()

