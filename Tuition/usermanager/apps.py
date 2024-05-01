from django.apps import AppConfig
from django.conf import settings
from django.db import IntegrityError
import sys
class UsermanagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usermanager'


    def ready(self):
        from .models import Role
        if settings.INSERT_DATA and ( "runserver" in sys.argv or "gunicorn" in sys.argv) :
            print("Inserting Roles")
            try:
                Role.objects.create(roleId=1,roleName="user")
                Role.objects.create(roleId=2,roleName="manager")
                Role.objects.create(roleId=3,roleName="admin")
                print("Role created")
            except IntegrityError as e:
                print(e)
            
        