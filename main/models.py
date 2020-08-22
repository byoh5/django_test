from django.db import models

# Create your models here.
class RegisterTB(models.Model):
    regi_idx = models.AutoField(primary_key=True)
    regi_id = models.CharField(max_length=50)
    regi_name = models.CharField(max_length=50)
    regi_phone = models.CharField(max_length=50)
    regi_email = models.CharField(max_length=50)
    regi_add01 = models.CharField(max_length=50)
    regi_add02 = models.CharField(max_length=50)
    regi_add03 = models.CharField(max_length=50)
    regi_pass = models.CharField(max_length=50)
    dbstat = models.CharField(max_length=50,default='A')
 #   expireTime = models.DurationField()
 #   stime = models.DateTimeField()