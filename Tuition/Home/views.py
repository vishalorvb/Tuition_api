from django.shortcuts import render
from .HomeBAL import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from usermanager.service import send_Email
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.decorators.csrf import csrf_exempt
import json
from utility.useful import encryption
from django.conf import settings
from django.core import serializers

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


def Home(request):
    tuitions = getTuition()
    return render(request, 'Home/home.html')


@login_required(login_url="/usermanager/login")
def profile(request):
    mytution = getMytuition(request.user.id)
    mytuitionunlock = getMyUnlockTuition(request.user.id)
    myteacher = getmyteacher(request.user.id)
    context = {"T": mytution, "UT": mytuitionunlock, "Teacher": myteacher}
    return render(request, 'Home/profile.html', context)


@login_required(login_url="/usermanager/login")
def editProfile(request):
    if request.method == "POST":
        user = request.user
        name = request.POST['name']
        if len(request.FILES) > 0:
            file = request.FILES['pic']
            file = reSizeImage(file, (500, 500))
            encypt = encryption(settings.SECRET_KEY)
            file.name = encypt.encrypt_string(str(user.id))
            user.profilepic = file
        user.Full_name = name
        user.save()
        return render(request, 'Home/profile.html')
    return render(request, 'Home/updateProfile.html')


def isPincode(request):
    pin = isPincodeExist(request.GET["pincode"])
    response = {"exist": pin}
    return HttpResponse(json.dumps(response), content_type="application/json")


def error(request):
    return render(request, 'Home/Errorpage.html')




def reSizeImage(input_image, output_size):
    image = Image.open(input_image)
    image = ImageOps.exif_transpose(image)
    image.thumbnail(output_size)
    image_io = BytesIO()
    image.save(image_io, format='JPEG')
    resized_image = InMemoryUploadedFile(
        image_io,
        None,
        'resized_image.jpg',
        'image/jpeg',
        image_io.tell(),
        None
    )
    return resized_image


def getPin(request):
    pin = request.GET["pincode"]
    matching_pincodes = getPincode(pin)
    data_list = list(matching_pincodes)
    json_data = json.dumps(data_list)
    return HttpResponse(json_data, content_type="application/json")

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def test(request):
    user = request.user
    print(user)
    return Response({"message": f"Hello, {user.Full_name}! This is a protected route."}, status=status.HTTP_200_OK)