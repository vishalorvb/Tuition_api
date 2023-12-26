from rest_framework import serializers
from .models import Teacher

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = fields = [
            'Name',
            'Gender',
            'Experience',
            'Location',
            'Qualification',
            'Subject',
            'classes',
            'About',
            'User_id',
            'Teaching_mode',
            'Phone_number',
            'Pincode',
            'Age',
            'Fee',
            'Photo',
        ]
