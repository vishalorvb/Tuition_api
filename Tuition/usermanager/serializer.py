from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'Full_name', 'email', 'credit_points', 'profilepic', 'is_teacher', 'is_email_varified',  'role']
