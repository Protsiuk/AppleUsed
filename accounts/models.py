from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


# from django.contrib.auth.models import User



# from utils import get_file_path


class User(AbstractUser):
    # username = models.CharField('username', max_length=255)
    email = models.EmailField('email', max_length=255, unique=True)
    # photo = models.FileField(upload_to=get_file_path)
    # locations = models.CharField('locations', max_length=255)
    birth_day = models.DateField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # REQUIRED_FIELDS = ['email', 'password']

    class Meta:
        swappable = "AUTH_USER_MODEL"

    # def email_user(self, *args, **kwargs):
    #     send_mail(
    #         '{}'.format(args[0]),
    #         '{}'.format(args[1]),
    #         '{}'.format(args[2]),
    #         [self.email],
    #         fail_silently=False,
    #     )


class WebsiteSettings(models.Model):
    title = models.CharField(max_length=255)
    # favicon = models.ImageField(width_field=30, height_field=30)
    description = models.CharField(max_length=255)
    about = models.TextField(max_length=510)


class UserProfile(models.Model):
    # user = models.ForeignKey(User, related_name='profile')
    # user = models.ForeignKey(User)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    city = models.CharField(default='', blank=True, null=True, max_length=255)
    # city = models.ForeignKey(City,related_name='city', blank=True, null=True, help_text=_('Select your City')
    # location = models.ForeignKey(Country, related_name='location', blank=True, null=True, help_text=_('Select your Location'))
    phone = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


    # def create_profile(sender, **kwargs):
    #     if kwargs['created']:
    #         user_profile = UserProfile.objects.create(user=kwargs['instance'])

    # post_save.connnect(create_profile, sender=User)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.UserProfile.save()
        # instance.profile.save()


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


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(max_length=500, blank=True)
#     location = models.CharField(max_length=30, blank=True)
#     birth_date = models.DateField(null=True, blank=True)
#
#     @receiver(post_save, sender=User)
#     def create_user_profile(sender, instance, created, **kwargs):
#         if created:
#             Profile.objects.create(user=instance)
#
#     @receiver(post_save, sender=User)
#     def save_user_profile(sender, instance, **kwargs):
#         instance.profile.save()
