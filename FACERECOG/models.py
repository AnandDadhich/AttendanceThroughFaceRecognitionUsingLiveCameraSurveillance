from django.db import models
from django.contrib.auth.models import User
from USERS.models import Profile
from PIL import Image
# Create your models here.

class EmployeeInfo(models.Model):
    id=models.IntegerField(primary_key=True,null=False,blank=False)
    name=models.CharField(null=False,blank=False,max_length=30)
    date_created=models.DateTimeField(auto_now_add=True)
    #usr=models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AboutEmployees(models.Model):
    memname=models.CharField(null=True,blank=True,max_length=30)
    memimage=models.ImageField(default='default.jpg',upload_to='profile_pics')

    def __str__(self):
        return self.memname

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

        img=Image.open(self.memimage.path)

        if img.height > 300 or img.width > 300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.memimage.path)

class ContactUs(models.Model):
    name=models.CharField(max_length=30)
    phone=models.CharField(max_length=10)
    email=models.EmailField(max_length=254)
    message=models.CharField(max_length=400)

    def __str__(self):
        return f' {self.name} '