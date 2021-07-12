from django.db import models
from django.contrib.auth.models import User


# Create your models here.



class Userinfo(models.Model):
    nametext=models.CharField(max_length=10)
    birdate=models.DateField(null=True)
    zwtext=models.CharField(max_length=10)
    zwdate=models.DateField(null=True)
    djtext=models.CharField(max_length=10)
    djdate=models.DateField(null=True)
    zctext=models.CharField(max_length=10)
    zcdate=models.DateField(null=True)
    dwtext=models.CharField(max_length=40)
    ryimage=models.ImageField(verbose_name="ryimage",null=True,upload_to="img/",blank=True)
    owner=models.OneToOneField(User,on_delete=models.CASCADE)






