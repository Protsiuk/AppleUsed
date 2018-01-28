from django.db import models

from django.contrib.auth.models import AbstractUser

# from utils import get_file_path


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    # photo = models.FileField(upload_to=get_file_path)
    birth_day = models.DateField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        swappable = "AUTH_USER_MODEL"


class WebsiteSettings(models.Model):
    title = models.CharField(max_length=255)
    # favicon = models.ImageField(width_field=30, height_field=30)
    description = models.CharField(max_length=255)
    about = models.TextField(max_length=510)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    city = models.CharField(default='', blank=True, null=True, max_length=255)
    # city = models.ForeignKey(City,related_name='city', blank=True, null=True, help_text=_('Select your City')
    # location = models.ForeignKey(Country, related_name='location', blank=True, null=True, help_text=_('Select your Location'))
    phone = models.IntegerField(default=0)

    # def create_profile(sender, **kwargs):
    #     if kwargs['created']:
    #         user_profile = UserProfile.objects.create(user=kwargs['instance'])

    # post_save.connnect(create_profile, sender=User)

# # Create your models here.
# class Member (models.Model):
#     username = models.CharField(max_length= 255)
#     password = models.CharField(max_length= 255)
#     email = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.username
#
#     def upper_username(self):
#         return self.username.upper()
