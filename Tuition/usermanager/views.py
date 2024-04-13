

from django.contrib.auth import authenticate
import logging
from .usermanagerBAL import *
import urllib.parse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    filename='../info.log', filemode='a', datefmt='%d-%b-%y %H:%M:%S')



#############################################################
######################## API ################################
#############################################################





@api_view(['POST'])
def createUser(request):
    try:
        full_name = request.data['full_name']
        email = request.data['email']
        phone_number = request.data['phone_number']
        res = saveUser(full_name, email, phone_number)
        if res == False:
            message = "User created successfully."
            return Response({"message": message}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": res}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
            logging.exception("Registration post request")
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    


def updateProfile(request):
    pass


@api_view(['POST'])
def sendOtp(request):
    try:
        phone_number = request.data['phone_number']
        if updatePassword(phone_number):
            message = "OTP sent successfully."
            return Response({"message": message}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid phone number."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception:
            logging.exception("Registration post request")
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    user =  authenticate( phone_number=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        response_data = {
            #'refresh': str(refresh),
            'access': str(refresh.access_token),
            'Full_name': user.Full_name,
            'roleId': user.role.roleId,
            'isTeacher': user.is_teacher
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    


@api_view(['GET'])
def verify_email(request, link):
    try:
        val = verifyEmail(urllib.parse.unquote(link))
        if val:
            return Response({"detail": "Verified"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Fail"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logging.exception("Registration post request")
        return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([AllowAny])  
def refreshToken(request):
    refresh_token_value = request.data.get('refresh_token')

    if not refresh_token_value:
        return Response({'message': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh_token = RefreshToken(refresh_token_value)
        access_token = str(refresh_token.access_token)
        response_data = {
            'refresh': str(refresh_token),
            'access': access_token,
        }
        return Response({'token': response_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Invalid refresh token: {e}'}, status=status.HTTP_400_BAD_REQUEST)