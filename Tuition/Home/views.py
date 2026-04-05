from django.shortcuts import render
from .HomeBAL import *
from usermanager.service import send_Email
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


def Home(request):
    return render(request, 'home.html')
 

@api_view(['GET'])
def getPin(request):
    pin = request.GET["pincode"]
    matching_pincodes = getPincode(pin)
    return Response(matching_pincodes, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def test(request):
    user = request.user
    print(user)
    return Response({"message": f"Hello, {user.Full_name}! This is a protected route."}, status=status.HTTP_200_OK)