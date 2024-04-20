
from .tuitionBAL import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializer import TuitionsSerializer,TuitionsSerializer_withPhone
from utility.ResizeImage import reSizeImage

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
        pincode = request.data.get('pincode',0)
        locality = request.data.get('locality','online')
        pin = isPincodeExists(pincode)
        image_file = request.FILES.get('photo', None)
        if image_file is not None:
           image_file =  reSizeImage(image_file, (500, 500),str(request.user.id))
    except KeyError:
        logging.exception("post tuition")
        return Response({"message": "Invalid Data format."}, status=status.HTTP_400_BAD_REQUEST)
    if pin == False:
        return Response({"message": "Invalid pincode."}, status=status.HTTP_400_BAD_REQUEST)
    
    t = saveTuition(request.user, student_name=student_name, phone_number=phone_number, course=course, subject=subject, description=description, teaching_mode=mode, fee=fee,pincode=pin,locality=locality,photo=image_file)

    if t:
        return Response({"message": "Your Tuition Posted Successfully.","tuitionId":t}, status=status.HTTP_201_CREATED)
    return Response({"message": "Failed to create."}, status=status.HTTP_400_BAD_REQUEST)






@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def unlockTuition(request):
    try:
        tuition_id = request.data['tuition_id']
        contact = unlock_tuitions(request.user,tuition_id)
        if contact:
            return Response({"message": "Succesfull","contact":contact}, status=status.HTTP_200_OK)
        return Response({"message": "Failed to get contact.","contact":None}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"message": "Invalid Data.","contact":None}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def changeStatus(request):
    try:
        tid = request.data['tuition_id']
        t  = change_status_of_tuition(request.user.id,tid)
        if t:
            return Response({"message": "Opration Successfull."}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid attempt"}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response({"message": "Invalid Data format."}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def getLatestTuition(request,pageNumber):
    tuition =  get_latest_tuition(pageNumber)
    data = TuitionsSerializer_withPhone(tuition, many=True).data
    return Response({"message": "Latest Tuition.", "data": data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_tution_byId(request,tuitionId):
    #geeting tuition by tuiionId
    tuition  = getTution_deatils(tuitionId)

    #return none if no tuition found of given tuitionId
    if tuition is None:
        return Response({"message": "No tuition found", "data": None}, status=status.HTTP_200_OK)
    

    if request.user.is_authenticated and canPhoneNumber(tuition.id, request.user.id):
        return Response({"message": "Authenticated user.", "data": TuitionsSerializer_withPhone(tuition).data}, status=status.HTTP_200_OK)

    return  Response({"message": "UnAuthenticated user.", "data": TuitionsSerializer_withPhone(tuition).data}, status=status.HTTP_200_OK) # change it to tuition without phone in next release

@api_view(['GET'])
def search(request,pageNumber):
    query = request.query_params.get('query', '')
     # Split the query into individual words
    query_words = query.split()

    t = search_tuitions(query_words,pageNumber)
    return Response({"message": "Search result.", "data": TuitionsSerializer_withPhone(t,many=True).data}, status=status.HTTP_200_OK) # change it to without phone number in next release


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def unlockedtuition(request):
    tuitions = unlockedTuitionBAL(request.user)
    return Response({ "data": TuitionsSerializer_withPhone(tuitions, many=True).data}, status=status.HTTP_200_OK)




@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def userPostedTuition(request):
    tuitions = userPost(request.user.id)
    return Response({ "data": TuitionsSerializer_withPhone(tuitions, many=True).data}, status=status.HTTP_200_OK)