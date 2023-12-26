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
                    filename='../info.log', filemode='a', datefmt='%d-%b-%y %H:%M:%S')




def getorderdetails(request):
    if request.method == "GET":
        try:
            plan_code = request.GET["plan"] 
        except Exception:
            logging.exception("name change of plan")
            return HttpResponseRedirect(reverse('Home:error'))
        
        # checking is plan code exist or not 
        plan = is_plan_exist(plan_code)
        if plan == False:
            logging.info("plan code not exist")
            return HttpResponseRedirect(reverse('Home:error'))
        
        if request.user.is_authenticated:
            callback_url = '/payment/verify_payment'
            context = create_order(request.user,plan.price,plan)
            if context:
                context['callback_url'] = callback_url
                return JsonResponse(context)
        else:
            context = {
                    "name":"none"
                } 
            request.session['redirect_url_name'] = '/payment/create_order' 
            return JsonResponse(context) 
             
    
# @login_required(login_url="/usermanager/login")
def Create_payment_order(request):
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
 
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            temp = verify_paymentBAL(params_dict)
            if temp:
                return HttpResponseRedirect(reverse('Home:profile'))
            else:
                return HttpResponseRedirect(reverse('Home:error'))
            
           
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

