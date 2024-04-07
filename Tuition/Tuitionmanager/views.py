
from .tuitionBAL import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializer import TuitionsSerializer,TuitionsSerializer_withPhone


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
        pincode = 0 if request.data.get('pincode') == None else request.data.get('pincode')
        locality = " " if request.data.get('locality') == None else request.data.get('locality')
        pin = isPincodeExists(pincode)
    except:
        logging.exception("post tuition")
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


@api_view(['GET'])
def getLatestTuition(request,pageNumber):
    tuition =  get_latest_tuition(pageNumber)
    data = TuitionsSerializer(tuition, many=True).data
    return Response({"message": "Operation Successful.", "data": data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_tution_byId(request,tuitionId):
    #geeting tuition by tuiionId
    tuition  = getTution_deatils(tuitionId)

    #return none if no tuition found of given tuitionId
    if tuition is None:
        return Response({"message": "No tuition found", "data": None}, status=status.HTTP_200_OK)
    


    if request.user.is_authenticated and canPhoneNumber(tuition.id, request.user.id):
        return Response({"message": "Authenticated user.", "data": TuitionsSerializer(tuition).data}, status=status.HTTP_200_OK)

    return  Response({"message": "Authenticated user.", "data": TuitionsSerializer_withPhone(tuition).data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def search(request):
    query = request.query_params.get('query', '')
     # Split the query into individual words
    query_words = query.split()

    t = search_tuitions(query_words)
    return Response({"message": "Authenticated user.", "data": TuitionsSerializer(t,many=True).data}, status=status.HTTP_200_OK)