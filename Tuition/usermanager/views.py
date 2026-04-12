

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

logger = logging.getLogger(__name__)



#############################################################
######################## API ################################
#############################################################





@api_view(['POST'])
def createUser(request):
    logger.info("createUser: Request received")
    required_fields = ['full_name', 'email', 'phone_number']
    missing = [f for f in required_fields if f not in request.data]
    if missing:
        logger.warning("createUser: Missing fields - %s", ', '.join(missing))
        return Response({"message": f"Missing fields: {', '.join(missing)}"}, status=status.HTTP_400_BAD_REQUEST)

    logger.info("createUser: Calling saveUser for phone=%s, email=%s", request.data['phone_number'], request.data['email'])
    error = saveUser(request.data['full_name'], request.data['email'], request.data['phone_number'])
    if error:
        logger.error("createUser: Failed - %s", error)
        return Response({"message": error}, status=status.HTTP_400_BAD_REQUEST)
    logger.info("createUser: User created successfully for phone=%s", request.data['phone_number'])
    return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    logger.info("updateProfile: Request received for userId=%s", request.user.id)
    try:
        full_name = request.data['full_name']
        email = request.data['email']
        logger.info("updateProfile: Fetching user data for userId=%s", request.user.id)
        user = getUserdata(request.user.id)
        if user.email != email and isEmailexist(email):
            logger.warning("updateProfile: Email %s already exists for another user", email)
            return Response({"message": "Email already exist"}, status=status.HTTP_400_BAD_REQUEST) 
        image_file = request.FILES.get('photo', None)
        if image_file:
            logger.info("updateProfile: Resizing profile image for userId=%s", request.user.id)
            image_file = reSizeImage(image_file, (500, 500), str(request.user.id))
        
        user.Full_name = full_name
        user.email = email
        user.profilepic = image_file
        user.save()
        logger.info("updateProfile: Profile updated successfully for userId=%s", request.user.id)
        return Response({"message": "Profile updated"}, status=status.HTTP_200_OK)
    except KeyError:
        logger.error("updateProfile: Invalid data format - missing required fields")
        return Response({"message": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST) 
    



@api_view(['POST'])
def sendOtp(request):
    logger.info("sendOtp: Request received")
    phone_number = request.data.get('phone_number')
    if not phone_number:
        logger.warning("sendOtp: phone_number is missing")
        return Response({"message": "phone_number is required"}, status=status.HTTP_400_BAD_REQUEST)

    logger.info("sendOtp: Calling updatePassword for phone=%s", phone_number)
    if updatePassword(phone_number):
        logger.info("sendOtp: OTP sent successfully to phone=%s", phone_number)
        return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
    logger.error("sendOtp: Failed to send OTP to phone=%s", phone_number)
    return Response({"message": "Invalid phone number."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    logger.info("login: Request received")
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        logger.warning("login: Missing username or password")
        return Response({"message": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    logger.info("login: Authenticating user phone=%s", username)
    user = authenticate(phone_number=username, password=password)
    if not user:
        logger.warning("login: Authentication failed for phone=%s", username)
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    response_data = {
        'access': str(refresh.access_token),
        'Full_name': user.Full_name,
        'roleId': user.role.roleId,
        'isTeacher': user.is_teacher,
        'userId': user.id,
    }
    logger.info("login: Login successful for userId=%s", user.id)
    return Response({"message": "Login successfull!", "data": response_data}, status=status.HTTP_200_OK)
    


@api_view(['GET'])
def verify_email(request, link):
    logger.info("verify_email: Request received")
    try:
        val = verifyEmail(urllib.parse.unquote(link))
        if val:
            logger.info("verify_email: Email verified successfully")
            return Response({"detail": "Verified"}, status=status.HTTP_200_OK)
        else:
            logger.warning("verify_email: Verification failed - invalid link")
            return Response({"detail": "Fail"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.exception("verify_email: Unexpected error - %s", str(e))
        return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([AllowAny])  
def refreshToken(request):
    logger.info("refreshToken: Request received")
    refresh_token_value = request.data.get('refresh_token')

    if not refresh_token_value:
        logger.warning("refreshToken: Refresh token is missing")
        return Response({'message': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh_token = RefreshToken(refresh_token_value)
        access_token = str(refresh_token.access_token)
        response_data = {
            'refresh': str(refresh_token),
            'access': access_token,
        }
        logger.info("refreshToken: Token refreshed successfully")
        return Response({'token': response_data}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error("refreshToken: Invalid refresh token - %s", str(e))
        return Response({'error': f'Invalid refresh token: {e}'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getUserinfo(request):
    logger.info("getUserinfo: Request received for userId=%s", request.user.id)
    user = getUserdata(request.user.id)
    logger.info("getUserinfo: Returning user data for userId=%s", request.user.id)
    return Response({ "data": UserSerializer(user).data}, status=status.HTTP_200_OK)