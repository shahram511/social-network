import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
<<<<<<< HEAD
#this change
=======

>>>>>>> 4a89704 (initatl commit)
# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=100)
    abbr = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        db_table = 'countries' #if we dont specify the table name, it will be the accounts_country

class Profile(models.Model):
    
    choice = ["france", "germany", "italy", "spain", "portugal", "belgium", "netherlands", "austria", "switzerland"]
    choice_list = [(i, i) for i in choice]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, unique=True,blank=True,null=True)
    country = models.CharField(max_length=100, choices=choice_list, default='france')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        db_table = 'profiles'
        
    def __str__(self):
        return f"{self.user.username} - {self.country}"
    
class Device(models.Model):
    DEVICE_WEB = 1
    DEVICE_ANDROID = 2
    DEVICE_IOS = 3
    DIVICE_PC = 4
    DEVICE_CHOICES = [
        (DEVICE_WEB, 'Web'),
        (DEVICE_ANDROID, 'Android'),
        (DEVICE_IOS, 'IOS'),
        (DIVICE_PC, 'PC'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='devices')
    device_uuid = models.UUIDField('device UUID',unique=True, default=uuid.uuid4)
    last_login = models.DateTimeField('last login date',auto_now=True)
    device_type = models.PositiveSmallIntegerField(choices=DEVICE_CHOICES, default=DEVICE_WEB)
    device_os = models.CharField('device os',max_length=100, blank=True, null=True)
    device_model = models.CharField('device model',max_length=100, blank=True, null=True)
    app_version = models.CharField('app version',max_length=100, blank=True, null=True)
    created_at = models.DateTimeField('created date',auto_now_add=True)
    
    class Meta:
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'
        db_table = 'devices'
        
    def __str__(self):
        return f"{self.user.username} - {self.device_uuid}"
    

<<<<<<< HEAD
    
=======
    
>>>>>>> 4a89704 (initatl commit)
