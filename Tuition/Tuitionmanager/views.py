
from .tuitionBAL import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',
                    filename='../info.log', filemode='a', datefmt='%d-%b-%y %H:%M:%S')


        


##################################################################################
################################## API ###########################################
##################################################################################
    
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def createTuition(request):
    try:
        student_name = request.data['student_name']
        phone_number = request.data['student_phone_number']
        course = request.data['course']
        subject = request.data['subject']
        description = request.data['description']
        fee = request.data['fee']
        mode = request.data['mode']
        pincode = request.data['pincode']
        locality = request.data['locality']
        pin = isPincodeExists(pincode)
    except:
        return Response({"message": "Invalid Data format."}, status=status.HTTP_400_BAD_REQUEST)
    if pin == False:
        return Response({"message": "Invalid pincode."}, status=status.HTTP_400_BAD_REQUEST)
    
    t = saveTuition(request.user, student_name=student_name, phone_number=phone_number, course=course, subject=subject, description=description, teaching_mode=mode, fee=fee,pincode=pin,locality=locality)

    if t:
        return Response({"message": "Your Tuition Posted Successfully."}, status=status.HTTP_201_CREATED)
    return Response({"message": "Failed to create."}, status=status.HTTP_400_BAD_REQUEST)






@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def unlockTuition(request):
    try:
        tuition_id = request.data['tuition_id']
        contact = unlock_tuitions(request.user,tuition_id)
        if contact:
            return Response({"message": contact}, status=status.HTTP_200_OK)
        Response({"message": "Failed to get contact."}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"message": "Invalid Data."}, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def changeStatus(request):
    try:
        tid = request.GET['tuition_id']
        t  = change_status_of_tuition(request.user.id,tid)
        if t:
            return Response({"message": "Opration Successfull."}, status=status.HTTP_200_OK)
        Response({"message": "Failed."}, status=status.HTTP_400_BAD_REQUEST)

    except:
        Response({"message": "Invalid Data."}, status=status.HTTP_400_BAD_REQUEST)



def getTuition(request):
    pass
