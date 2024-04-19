from django.shortcuts import render
from .TeacherBAL import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
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
        if image_file is not None:
           image_file =  reSizeImage(image_file, (500, 500),str(user.id))
        Name = request.data['teacher_name']
        Gender = request.data['gender']
        Experience = request.data['experience']
        Location = request.data.get('location',"online")
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
        
        teacher = save_teacher(name=Name, gender=Gender, experience=Experience,
                                   location=Location, qualification=Qualification, subject=Subject, classes=classes,
                                   about=About, user_id=User_id, teaching_mode=Teaching_mode,
                                   phone_number=request.user.phone_number,
                                   age=Age, fee=Fee, pincode=pin,photo=image_file)
        if teacher:
            message = "Register as teacher succefully."
            return Response({"message": message,"teacherId":teacher.id}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Failed to create."}, status=status.HTTP_400_BAD_REQUEST)

    except KeyError:
        logging.exception("Registration post request")
        return Response({"message": "Invalid data format"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_teacher_Profile(request): 
  
    try:
        #checking techer exit ot not for a given teacherID 
        Teacher = is_teacher_exist(request.data['id'])
        if Teacher == False :
            return Response({"message": "Invalid teacher ID."}, status=status.HTTP_400_BAD_REQUEST)
        
        #checking techer belong to logged in user
        if Teacher.user_id.id != request.user.id:
            return Response({"message": "Teacher not belogs to user."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        
        image_file = request.FILES.get('photo', None)
        if image_file :
           image_file =  reSizeImage(image_file, (500, 500),str(request.user.id))
           Teacher.photo = image_file
        Teacher.name = request.data['name']
        Teacher.experience = request.data['experience']
        Teacher.location = request.data['location']
        Teacher.qualification = request.data['qualification']
        Teacher.subject = request.data['subject']
        Teacher.classes = request.data['classes']
        Teacher.pincode =isPincode(request.data.get('pincode',0))
        Teacher.teaching_mode = request.data['mode']
        Teacher.age = request.data['age']
        Teacher.about = request.data['about']
        Teacher.save()
        return Response({"message": "Teacher Profile Updated."}, status=status.HTTP_202_ACCEPTED)
    except KeyError:
        logging.exception("create teacher in view")
        return Response({"message": "Invalid Data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


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


@api_view(['GET'])
def get_Teacher_ById(request,teacherId):
    teacher = getTeacher(teacherId)
    if teacher is None:
        return Response({"message": "No Teacher found", "data": None}, status=status.HTTP_200_OK)
    if request.user.is_authenticated and canPhoneNumber(request.user,teacherId):
        return Response({"message": "Authenticated user.", "data": TeacherSerializerWithphone(teacher).data}, status=status.HTTP_200_OK)
    return Response({"message": "UnAuthenticated user.", "data": TeacherSerializerWithphone(teacher).data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def search(request,pageNumber):
    query = request.query_params.get('query', '')
     # Split the query into individual words
    query_words = query.split()
    t = search_Teacher(query_words,pageNumber)
    return Response({"message": "Authenticated user.", "data": TeacherSerializer(t,many=True).data}, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def unlocked_teacher(request):
    teacher = unlockedTeacher(request.user.id)
    return Response({"message": "Authenticated user.", "data": TeacherSerializerWithphone(teacher,many=True).data}, status=status.HTTP_200_OK)