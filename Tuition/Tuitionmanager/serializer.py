

from rest_framework import serializers
from .models import Tuitions
from Home.serializer import PincodeSerializer
from datetime import datetime


class DateCoerceField(serializers.DateField):
    def to_representation(self, value):
        if isinstance(value, datetime):
            value = value.date()
        return super().to_representation(value)


# This will serialize all data INCLUDE PHONE number
class TuitionsSerializer(serializers.ModelSerializer):
    pincode_info = PincodeSerializer(source='pincode', read_only=True)
    posted_date = DateCoerceField(format='%Y-%m-%d')
    class Meta:
        model = Tuitions
        fields = ['id','posted_date', 'teaching_mode','student_name',  'course', 'subject', 'description',  'fee', 'pincode_info', 'locality', 'unlocks', 'verify', 'slug','pincode','status']


# This will serialize all data WITHOUT PHONE number     
class TuitionsSerializer_withPhone(serializers.ModelSerializer):
    pincode_info = PincodeSerializer(source='pincode', read_only=True)
    posted_date = DateCoerceField(format='%Y-%m-%d')
    class Meta:
        model = Tuitions
        fields = ['id','posted_date', 'teaching_mode', 'student_name',"phone_number", 'course', 'subject', 'description',  'fee', 'pincode_info', 'locality', 'unlocks', 'verify', 'slug','pincode','status']