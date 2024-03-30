from rest_framework import serializers
from .models import pincodes


class PincodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = pincodes
        fields = ['Pincode', 'Devision', 'Region', 'Circle', 'Taluk', 'District', 'State']