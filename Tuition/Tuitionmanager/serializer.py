

from rest_framework import serializers
from .models import Tuitions
from Home.serializer import PincodeSerializer


# This will serialize all data INCLUDE PHONE number
class TuitionsSerializer(serializers.ModelSerializer):
    pincode_info = PincodeSerializer(source='pincode', read_only=True)
    class Meta:
        model = Tuitions
        fields = ['id','posted_date', 'student_name',  'course', 'subject', 'description',  'fee', 'pincode_info', 'locality', 'unlocks', 'verify', 'slug','pincode']


# This will serialize all data WITHOUT PHONE number     
class TuitionsSerializer_withPhone(serializers.ModelSerializer):
    pincode_info = PincodeSerializer(source='pincode', read_only=True)
    class Meta:
        model = Tuitions
        fields = ['id','posted_date', 'student_name',"phone_number", 'course', 'subject', 'description',  'fee', 'pincode_info', 'locality', 'unlocks', 'verify', 'slug','pincode']