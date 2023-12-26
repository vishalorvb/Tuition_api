from django.db import models

class pincodes(models.Model):
    Pincode = models.IntegerField(primary_key=True)
    Devision = models.CharField(max_length=100,null=False)
    Region = models.CharField(max_length=100,null=False)
    Circle = models.CharField(max_length=100,null=False)
    Taluk = models.CharField(max_length=100,null=False)
    District = models.CharField(max_length=100,null=False)
    State = models.CharField(max_length=100,null=False)
    
    def __str__(self):
        return str(self.Pincode)