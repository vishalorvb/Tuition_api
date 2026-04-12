from django.shortcuts import render
from .TeacherBAL import *
from .TeacherBAL import get_my_teacher_by_userid
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from utility.ResizeImage import reSizeImage
import logging

logger = logging.getLogger(__name__)



#############################################################
########################### API #############################
#############################################################



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_teacher(request):
    logger.info("create_teacher: Request received for userId=%s", request.user.id)
    user = request.user
    try:
        image_file = request.FILES.get('photo', None)
        if image_file is not None:
            logger.info("create_teacher: Resizing photo for userId=%s", user.id)
            image_file = reSizeImage(image_file, (500, 500), str(user.id))
        Name = request.data['teacher_name']
        Gender = request.data['gender']
        Experience = request.data['experience']
        Location = request.data.get('location', "online")
        Qualification = request.data['qualification']
        Subject = request.data['subject']
        classes = request.data['classes']
        About = request.data['about']
        User_id = request.user
        Teaching_mode = request.data['mode']
        Age = request.data['age']
        Fee = request.data['fee']
        Pincode = request.data.get('pincode', 0)
        pin = isPincode(Pincode)
        
        logger.info("create_teacher: Saving teacher profile for userId=%s, name=%s", user.id, Name)
        teacher = save_teacher(name=Name, gender=Gender, experience=Experience,
                                   location=Location, qualification=Qualification, subject=Subject, classes=classes,
                                   about=About, user_id=User_id, teaching_mode=Teaching_mode,
                                   phone_number=request.user.phone_number,
                                   age=Age, fee=Fee, pincode=pin, photo=image_file)
        if teacher:
            logger.info("create_teacher: Teacher created successfully teacherId=%s for userId=%s", teacher.id, user.id)
            message = "Register as teacher succefully."
            return Response({"message": message, "teacherId": teacher.id}, status=status.HTTP_201_CREATED)
        else:
            logger.error("create_teacher: Failed to create teacher for userId=%s", user.id)
            return Response({"message": "Failed to create."}, status=status.HTTP_400_BAD_REQUEST)

    except KeyError:
        logger.exception("create_teacher: Invalid data format for userId=%s", user.id)
        return Response({"message": "Invalid data format"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_teacher_Profile(request, teacherId): 
    logger.info("update_teacher_Profile: Request received for userId=%s teacherId=%s", request.user.id, teacherId)
    try:
        Teacher = getTeacheInfo(request.user.id, teacherId)
        if Teacher is None:
            logger.warning("update_teacher_Profile: Teacher not found for userId=%s teacherId=%s", request.user.id, teacherId)
            return Response({"message": "Teacher Not Exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        image_file = request.FILES.get('photo', None)
        if image_file:
            logger.info("update_teacher_Profile: Resizing photo for userId=%s", request.user.id)
            image_file = reSizeImage(image_file, (500, 500), str(request.user.id))
        Teacher.photo = image_file
        Teacher.name = request.data['teacher_name']
        Teacher.experience = request.data['experience']
        Teacher.location = request.data['location']
        Teacher.qualification = request.data['qualification']
        Teacher.subject = request.data['subject']
        Teacher.classes = request.data['classes']
        Teacher.pincode = isPincode(request.data.get('pincode', 0))
        Teacher.teaching_mode = request.data['mode']
        Teacher.age = request.data['age']
        Teacher.about = request.data['about']
        Teacher.save()
        logger.info("update_teacher_Profile: Profile updated for userId=%s", request.user.id)
        return Response({"message": "Teacher Profile Updated."}, status=status.HTTP_202_ACCEPTED)
    except KeyError:
        logger.exception("update_teacher_Profile: Invalid data for userId=%s", request.user.id)
        return Response({"message": "Invalid Data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getTecher_info(request, teacherId):
    logger.info("getTecher_info: Request received for userId=%s teacherId=%s", request.user.id, teacherId)
    teacher = getTeacheInfo(request.user.id, teacherId)
    if teacher == None:
        logger.warning("getTecher_info: Teacher not found for userId=%s teacherId=%s", request.user.id, teacherId)
        return Response({"message": "Teacher Not Exists."}, status=status.HTTP_400_BAD_REQUEST)
    logger.info("getTecher_info: Returning teacher info for userId=%s teacherId=%s", request.user.id, teacherId)
    serializer = TeacherSerializerWithphone(teacher)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def unlock_teacher(request):
    logger.info("unlock_teacher: Request received for userId=%s", request.user.id)
    try:
        teacherId = request.data["teacher_id"]
        logger.info("unlock_teacher: Unlocking teacherId=%s for userId=%s", teacherId, request.user.id)
        contact = unlock_teacherBAL(request.user, teacherId)
        if contact:
            logger.info("unlock_teacher: Successfully unlocked teacherId=%s", teacherId)
            return Response({"message": "Succesfull", "contact": contact}, status=status.HTTP_200_OK)
        logger.warning("unlock_teacher: Failed to unlock teacherId=%s", teacherId)
        return Response({"message": "Failed to get contact.", "contact": None}, status=status.HTTP_400_BAD_REQUEST)
    except:
        logger.exception("unlock_teacher: Invalid data for userId=%s", request.user.id)
        return Response({"message": "Invalid Data.", "contact": None}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getLatestTeacher(request, pageNumber):
    logger.info("getLatestTeacher: Request received page=%s", pageNumber)
    teacher = get_latest_teacher(pageNumber)
    data = TeacherSerializerWithphone(teacher, many=True).data
    logger.info("getLatestTeacher: Returning %s teachers", len(data))
    return Response({"message": "Operation Successful.", "data": data}, status=status.HTTP_200_OK) 


@api_view(['GET'])
def get_Teacher_ById(request, teacherId):
    logger.info("get_Teacher_ById: Request received teacherId=%s", teacherId)
    teacher = getTeacher(teacherId)
    if teacher is None:
        logger.warning("get_Teacher_ById: Teacher not found teacherId=%s", teacherId)
        return Response({"message": "No Teacher found", "data": None}, status=status.HTTP_200_OK)
    if request.user.is_authenticated and canPhoneNumber(request.user, teacherId):
        logger.info("get_Teacher_ById: Authenticated access for teacherId=%s", teacherId)
        return Response({"message": "Authenticated user.", "data": TeacherSerializerWithphone(teacher).data}, status=status.HTTP_200_OK)
    logger.info("get_Teacher_ById: Unauthenticated access for teacherId=%s", teacherId)
    return Response({"message": "UnAuthenticated user.", "data": TeacherSerializerWithphone(teacher).data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def search(request, pageNumber):
    query = request.query_params.get('query', '').strip()
    logger.info("search: Request received query='%s' page=%s", query, pageNumber)
    if not query:
        logger.warning("search: Empty query")
        return Response({"message": "Query is required.", "data": [], "totalPages": 0}, status=status.HTTP_400_BAD_REQUEST)

    query_words = query.split()
    teachers, total_pages = search_Teacher(query_words, pageNumber)
    data = TeacherSerializer(teachers, many=True).data if teachers else []
    logger.info("search: Returning %s results, totalPages=%s", len(data), total_pages)
    return Response({"message": "Search result.", "data": data, "totalPages": total_pages}, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def unlocked_teacher(request):
    logger.info("unlocked_teacher: Request received for userId=%s", request.user.id)
    teacher = unlockedTeacher(request.user.id)
    logger.info("unlocked_teacher: Returning unlocked teachers for userId=%s", request.user.id)
    return Response({"message": "Authenticated user.", "data": TeacherSerializerWithphone(teacher, many=True).data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_my_teacher_profile(request):
    logger.info("get_my_teacher_profile: Request received for userId=%s", request.user.id)
    teachers = get_my_teacher_by_userid(request.user.id)
    logger.info("get_my_teacher_profile: Found %s profiles for userId=%s", len(teachers), request.user.id)
    serializer = TeacherSerializer(teachers, many=True)
    return Response({"teachers": serializer.data}, status=status.HTTP_200_OK)