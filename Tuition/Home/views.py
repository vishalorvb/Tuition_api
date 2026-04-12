from django.shortcuts import render
from .HomeBAL import *
from usermanager.service import send_Email
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def Home(request):
    logger.info("Home: Rendering home page")
    return render(request, 'home.html')
 

@api_view(['GET'])
def getPin(request):
    pin = request.GET["pincode"]
    logger.info("getPin: Searching pincodes starting with %s", pin)
    matching_pincodes = getPincode(pin)
    logger.info("getPin: Found %s matching pincodes", len(matching_pincodes))
    return Response(matching_pincodes, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def test(request):
    user = request.user
    logger.info("test: Protected route accessed by userId=%s", user.id)
    return Response({"message": f"Hello, {user.Full_name}! This is a protected route."}, status=status.HTTP_200_OK)