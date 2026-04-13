from django.db import models
from django.contrib.postgres.indexes import GinIndex

class pincodes(models.Model):
    Pincode = models.IntegerField(primary_key=True)
    Devision = models.CharField(max_length=100,null=False)
    Region = models.CharField(max_length=100,null=False)
    Circle = models.CharField(max_length=100,null=False)
    Taluk = models.CharField(max_length=100,null=False)
    District = models.CharField(max_length=100,null=False)
    State = models.CharField(max_length=100,null=False)

    class Meta:
        indexes = [
            GinIndex(
                name='pincode_trgm_idx',
                fields=['Devision', 'District', 'State', 'Taluk', 'Region'],
                opclasses=['gin_trgm_ops', 'gin_trgm_ops', 'gin_trgm_ops', 'gin_trgm_ops', 'gin_trgm_ops'],
            ),
        ]

    def __str__(self):
        return str(self.Pincode)