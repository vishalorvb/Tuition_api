from django.apps import AppConfig
from django.conf import settings
from django.db import IntegrityError

class UsermanagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usermanager'


    def ready(self):
        print("Inserting Roles")
        from .models import Role
        if settings.ENVIRONMENT_NAME == "prod":
            try:
                Role.objects.create(roleId=1,roleName="user")
                Role.objects.create(roleId=2,roleName="manager")
                Role.objects.create(roleId=3,roleName="admin")
            
            except IntegrityError as e:
                pass
            
        