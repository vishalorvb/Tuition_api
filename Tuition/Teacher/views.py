from django.shortcuts import render
from .TeacherBAL import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import TeacherSerializer
from utility.ResizeImage import reSizeImage



#############################################################
########################### API #############################
#############################################################



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_teacher(request):
    Teacher = is_user_teacher(request.user.id)
    user = request.user
    if Teacher:
        return Response({"message": "Already Exists."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        image_file = request.FILES.get('photo', None)
        print(image_file)
        if image_file is not None:
           image_file =  reSizeImage(image_file, (500, 500),str(user.id))
        Name = request.data['teacher_name']
        Gender = request.data['gender']
        Experience = request.data['experience']
        Location = request.data['location']
        Qualification = request.data['qualification']
        Subject = request.data['subject']
        classes = request.data['classes']
        About = request.data['about']
        User_id = request.user
        Teaching_mode = request.data['mode']
        Age = request.data['age']
        Fee = request.data['fee']
        Pincode = request.data.get('pincode',0)
        pin = isPincode(Pincode)
        
        teacher = save_teacher(Name=Name, Gender=Gender, Experience=Experience,
                                   Location=Location, Qualification=Qualification, Subject=Subject, classes=classes,
                                   About=About, User_id=User_id, Teaching_mode=Teaching_mode,
                                   Phone_number=request.user.phone_number,
                                   Age=Age, Fee=Fee, Pincode=pin,photo=image_file)
        if teacher:
            message = "Register as teacher succefully."
            return Response({"message": message}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Failed to create."}, status=status.HTTP_400_BAD_REQUEST)

    except:
        logging.exception("Registration post request")
        return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_teacher_Profile(request):
    Teacher = is_user_teacher(request.user.id)
    if Teacher == False:
        return Response({"message": "User is not a teacher."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        Teacher.Name = request.data['name']
        Teacher.Experience = request.data['experience']
        Teacher.Location = request.data['locality']
        Teacher.Qualification = request.data['qualification']
        Teacher.Subject = request.data['subject']
        Teacher.classes = request.data['classes']
        Teacher.Pincode =None if isPincode(request.data['pincode'])==False else isPincode(request.data['pincode'])
        Teacher.Teaching_mode = request.data['mode']
        Teacher.Age = request.data['age']
        Teacher.About = request.data['about']
        Teacher.save()
        return Response({"message": "Teacher Profile Updated."}, status=status.HTTP_202_ACCEPTED)
    except Exception:
        logging.exception("create teacher in view")
        return Response({"message": "Internal Server Error, Invalid Data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getTecher_info(request):
    teacher = getTeacheInfo(request.user.id)
    if teacher == None:
        return Response({"message": "Teacher Not Exists."}, status=status.HTTP_400_BAD_REQUEST)
    serializer = TeacherSerializer(teacher)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def unlock_teacher(request):
    try:
        teacherId = request.data["teacher_id"]
        contact = unlock_teacherBAL(request.user,teacherId)
        if contact:
            return Response({"message": "Succesfull","contact":contact}, status=status.HTTP_200_OK)
        return Response({"message": "Failed to get contact.","contact":None}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"message": "Invalid Data.","contact":None}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getLatestTeacher(request,pageNumber):
    teacher = get_latest_teacher(pageNumber)
    data = TeacherSerializer(teacher, many=True).data
    return Response({"message": "Operation Successful.", "data": data}, status=status.HTTP_200_OK) 


def get_Teacher_ById(request,teacherId):
    teacher = teacherId(teacherId)
    if teacher is None:
        return Response({"message": "No tuition found", "data": None}, status=status.HTTP_200_OK)