from django.apps import AppConfig
import csv
from django.db import IntegrityError
from django.conf import settings
import sys
class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Home'
    
    def ready(self):
        if settings.INSERT_DATA and ( "runserver" in sys.argv or "gunicorn" in sys.argv) :
            print("Inserting pincode!") 
            from .models import pincodes
            from .HomeDAL import isPincode
            with open('pincodes.csv', mode ='r')as file:
                csvFile = csv.reader(file)
                for lines in csvFile:
                    pincode, division, region, circle, taluk, district, state = lines
                    if(isPincode(pincode)):
                        try:
                            pincodes.objects.create(
                            Pincode=pincode,
                            Devision=division,
                            Region=region,
                            Circle=circle,
                            Taluk=taluk,
                            District=district,
                            State=state)
                            print("inserted="+pincode)
                        except IntegrityError as e:
                            pass
                        
