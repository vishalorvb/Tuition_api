

from django.contrib.auth import authenticate
import logging
from .usermanagerBAL import *
import urllib.parse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from utility.ResizeImage import reSizeImage

from  .serializer import UserSerializer
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')



#############################################################
######################## API ################################
#############################################################





@api_view(['POST'])
def createUser(request):
    required_fields = ['full_name', 'email', 'phone_number']
    missing = [f for f in required_fields if f not in request.data]
    if missing:
        return Response({"message": f"Missing fields: {', '.join(missing)}"}, status=status.HTTP_400_BAD_REQUEST)

    error = saveUser(request.data['full_name'], request.data['email'], request.data['phone_number'])
    if error:
        return Response({"message": error}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    try:
        full_name = request.data['full_name']
        email = request.data['email']
        user = getUserdata(request.user.id)
        if user.email != email and isEmailexist(email):
            return Response({"message": "Email already exist"}, status=status.HTTP_400_BAD_REQUEST) 
        image_file = request.FILES.get('photo', None)
        if image_file :
           image_file =  reSizeImage(image_file, (500, 500),str(request.user.id))
        
        user.Full_name = full_name
        user.email = email
        user.profilepic = image_file
        user.save()
        return Response({"message": "Profile updated"},status=status.HTTP_200_OK)
    except KeyError:
        return Response({"message": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST) 
    



@api_view(['POST'])
def sendOtp(request):
    phone_number = request.data.get('phone_number')
    otp_type = request.data.get('type', 'login')
    if not phone_number:
        return Response({"message": "phone_number is required"}, status=status.HTTP_400_BAD_REQUEST)
    if otp_type not in ('registration', 'login'):
        return Response({"message": "type must be 'registration' or 'login'"}, status=status.HTTP_400_BAD_REQUEST)

    if otp_type == 'registration':
        result = sendRegistrationOtp(phone_number)
    else:
        result = updatePassword(phone_number)

    if result:
        return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
    return Response({"message": "Invalid phone number."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"message": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(phone_number=username, password=password)
    if not user:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    response_data = {
        'access': str(refresh.access_token),
        'Full_name': user.Full_name,
        'roleId': user.role.roleId,
        'isTeacher': user.is_teacher,
        'userId': user.id,
    }
    return Response({"message": "Login successfull!", "data": response_data}, status=status.HTTP_200_OK)
    


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
    
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getUserinfo(request):
    user = getUserdata(request.user.id)
    return Response({ "data": UserSerializer(user).data}, status=status.HTTP_200_OK)