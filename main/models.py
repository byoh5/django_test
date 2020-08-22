from django.db import models

# Create your models here.
class RegisterTB(models.Model):
    regid = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    dbstat = models.CharField(max_length=50,default='A')
 #   expireTime = models.DurationField()
 #   stime = models.DateTimeField()