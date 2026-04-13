
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
logger = logging.getLogger(__name__)


        


##################################################################################
################################## API ###########################################
##################################################################################
    
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def createTuition(request):
    logger.info("createTuition: Request received for userId=%s", request.user.id)
    try:
        student_name = request.data['student_name']
        phone_number = request.data['student_phone_number']
        course = request.data['course']
        subject = request.data['subject']
        description = request.data['description']
        fee = request.data['fee']
        mode = request.data['mode']
        pincode = request.data.get('pincode', 0)
        locality = request.data.get('locality', 'online')
        pin = isPincodeExists(pincode)
        image_file = request.FILES.get('photo', None)
        if image_file is not None:
            logger.info("createTuition: Resizing photo for userId=%s", request.user.id)
            image_file = reSizeImage(image_file, (500, 500), str(request.user.id))
    except KeyError:
        logger.exception("createTuition: Missing required fields for userId=%s", request.user.id)
        return Response({"message": "Invalid Data format."}, status=status.HTTP_400_BAD_REQUEST)
    if pin == False:
        logger.warning("createTuition: Invalid pincode=%s for userId=%s", pincode, request.user.id)
        return Response({"message": "Invalid pincode."}, status=status.HTTP_400_BAD_REQUEST)
    
    logger.info("createTuition: Saving tuition for userId=%s, course=%s", request.user.id, course)
    t = saveTuition(request.user, student_name=student_name, phone_number=phone_number, course=course, subject=subject, description=description, teaching_mode=mode, fee=fee, pincode=pin, locality=locality, photo=image_file)

    if t:
        logger.info("createTuition: Tuition created tuitionId=%s for userId=%s", t, request.user.id)
        return Response({"message": "Your Tuition Posted Successfully.", "tuitionId": t}, status=status.HTTP_201_CREATED)
    logger.error("createTuition: Failed to create tuition for userId=%s", request.user.id)
    return Response({"message": "Failed to create."}, status=status.HTTP_400_BAD_REQUEST)






@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def unlockTuition(request):
    logger.info("unlockTuition: Request received for userId=%s", request.user.id)
    try:
        tuition_id = request.data['tuition_id']
        logger.info("unlockTuition: Unlocking tuitionId=%s for userId=%s", tuition_id, request.user.id)
        contact = unlock_tuitions(request.user, tuition_id)
        if contact:
            logger.info("unlockTuition: Successfully unlocked tuitionId=%s", tuition_id)
            return Response({"message": "Succesfull", "contact": contact}, status=status.HTTP_200_OK)
        logger.warning("unlockTuition: Failed to unlock tuitionId=%s", tuition_id)
        return Response({"message": "Failed to get contact.", "contact": None}, status=status.HTTP_400_BAD_REQUEST)
    except:
        logger.exception("unlockTuition: Invalid data for userId=%s", request.user.id)
        return Response({"message": "Invalid Data.", "contact": None}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def changeStatus(request):
    logger.info("changeStatus: Request received for userId=%s", request.user.id)
    try:
        tid = request.data['tuition_id']
        logger.info("changeStatus: Changing status for tuitionId=%s userId=%s", tid, request.user.id)
        t = change_status_of_tuition(request.user.id, tid)
        if t:
            logger.info("changeStatus: Status changed for tuitionId=%s", tid)
            return Response({"message": "Opration Successfull."}, status=status.HTTP_200_OK)
        logger.warning("changeStatus: Invalid attempt tuitionId=%s userId=%s", tid, request.user.id)
        return Response({"message": "Invalid attempt"}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        logger.error("changeStatus: Missing tuition_id in request")
        return Response({"message": "Invalid Data format."}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def getLatestTuition(request, pageNumber):
    logger.info("getLatestTuition: Request received page=%s", pageNumber)
    tuition = get_latest_tuition(pageNumber)
    data = TuitionsSerializer_withPhone(tuition, many=True).data
    logger.info("getLatestTuition: Returning %s tuitions", len(data))
    return Response({"message": "Latest Tuition.", "data": data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_tution_byId(request, tuitionId):
    logger.info("get_tution_byId: Request received tuitionId=%s", tuitionId)
    tuition = getTution_deatils(tuitionId)

    if tuition is None:
        logger.warning("get_tution_byId: Tuition not found tuitionId=%s", tuitionId)
        return Response({"message": "No tuition found", "data": None}, status=status.HTTP_200_OK)
    
    if request.user.is_authenticated and canPhoneNumber(tuition.id, request.user.id):
        logger.info("get_tution_byId: Authenticated access tuitionId=%s", tuitionId)
        return Response({"message": "Authenticated user.", "data": TuitionsSerializer_withPhone(tuition).data}, status=status.HTTP_200_OK)

    logger.info("get_tution_byId: Unauthenticated access tuitionId=%s", tuitionId)
    return Response({"message": "UnAuthenticated user.", "data": TuitionsSerializer_withPhone(tuition).data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def search(request, pageNumber):
    query = request.query_params.get('query', '').strip()
    location = request.query_params.get('location', '').strip()
    logger.info("search: Request received query='%s' location='%s' page=%s", query, location, pageNumber)
    if not query and not location:
        logger.warning("search: Empty query and location")
        return Response({"message": "Query or location is required.", "data": [], "totalPages": 0}, status=status.HTTP_400_BAD_REQUEST)

    tuitions, total_pages = search_tuitions(query, location, pageNumber)
    data = TuitionsSerializer(tuitions, many=True).data if tuitions else []
    logger.info("search: Returning %s results, totalPages=%s", len(data), total_pages)
    return Response({"message": "Search result.", "data": data, "totalPages": total_pages}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def unlockedtuition(request):
    logger.info("unlockedtuition: Request received for userId=%s", request.user.id)
    tuitions = unlockedTuitionBAL(request.user)
    logger.info("unlockedtuition: Returning unlocked tuitions for userId=%s", request.user.id)
    return Response({"data": TuitionsSerializer_withPhone(tuitions, many=True).data}, status=status.HTTP_200_OK)




@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def userPostedTuition(request):
    logger.info("userPostedTuition: Request received for userId=%s", request.user.id)
    tuitions = userPost(request.user.id)
    logger.info("userPostedTuition: Returning posted tuitions for userId=%s", request.user.id)
    return Response({"data": TuitionsSerializer_withPhone(tuitions, many=True).data}, status=status.HTTP_200_OK)