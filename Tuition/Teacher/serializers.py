from rest_framework import serializers
from .models import Teacher

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = fields = [
           'id',
            'name',
            'gender',
            'experience',
            'location',
            'qualification',
            'subject',
            'classes',
            'about',
            'teaching_mode',
            'pincode',
            'age',
            'fee',
            'photo',
        ]
