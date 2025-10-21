from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER ={
        (1,'admin'),
        (2,'driver'),
       
        
    }
    user_type = models.CharField(choices=USER,max_length=50,default=1)

    profile_pic = models.ImageField(upload_to='media/profile_pic')

class Driver(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    mobilenumber = models.CharField(max_length=11, unique=True)
    driverid = models.CharField(max_length=6, unique=True)
    address =  models.CharField(max_length=250)
    joinigdate_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Booking(models.Model):
    bookingnumber = models.IntegerField(default=0)
    fullname = models.CharField(max_length=250)
    email = models.EmailField(default=0)
    mobilenumber = models.CharField(max_length=11, unique=True)
    pickuplocation = models.CharField(max_length=250)
    destination = models.CharField(max_length=250)
    pickupdate = models.CharField(max_length=250)
    pickuptime = models.CharField(max_length=250)
    remark = models.CharField(max_length=250)
    status = models.CharField(max_length=250)
    assignto = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    bookingdate_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tracking(models.Model):
    booking_id =models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    remark = models.CharField(max_length=250)
    status = models.CharField(max_length=250)
    creationdate_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


