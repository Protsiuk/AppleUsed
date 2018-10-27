from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# from utils import get_file_path


class MyUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """Creates and saves users with the given email and password"""
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        # user.password = password # плохое решение
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class MyCustomUser(AbstractUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(max_length=254, unique=False, blank=True)
    # email = models.EmailField(max_length=255, unique=True)
    email = models.EmailField(
        _('Email Address'), unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    # photo = models.FileField(upload_to=get_file_path)
    birth_day = models.DateField(_('birth day'), blank=True, null=True)
    locations_user = models.CharField(default='', blank=True, null=True, max_length=512)
    # city = models.ForeignKey(City,related_name='city', blank=True, null=True, help_text=_('Select your City')
    # location = models.ForeignKey(Country, related_name='location', blank=True, null=True, help_text=_('Select your Location'))
    # phone = models.IntegerField(unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+9999999999'. Up to 15 digits allowed.")
    phone_number_user = models.CharField(validators=[phone_regex], max_length=15, blank=True)  # validators should be a list

    # phone = models.IntegerField(default=0, unique=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    # REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyUserManager()

    class Meta:
        swappable = "AUTH_USER_MODEL"
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    # def get_absolute_url(self):
    #     return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    # def email_user(self, subject, message, from_email=None):
    #     """
    #     Sends an email to this User.
    #     """
    #     send_mail(subject, message, from_email, [self.email])

#
# class UserManager(BaseUserManager):
#     def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
#         """Creates and saves users with the given email and password"""
#         now = timezone.now()
#         if not email:
#             raise ValueError('The given email must be set')
#
#         email = self.normalize_email(email)
#         user = self.model(email=email,
#                           is_staff=is_staff, is_active=True,
#                           is_superuser=is_superuser, last_login=now,
#                           date_joined=now, **extra_fields)
#         # user.password = password # плохое решение
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, email, password=None, **extra_fields):
#         return self._create_user(email, password, False, False, **extra_fields)
#
#     def create_superuser(self, email, password, **extra_fields):
#         return self._create_user(email, password, True, True, **extra_fields)


    # def create_user(self, username, email, password=None):
    #     if not email:
    #         raise ValueError('Введите пожалуйста Email')
    #     user = self.model(
    #                 username=username,
    #                 email=self.normalize_email(email)
    #             )
    #     # user.password = password # плохое решение
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user
    #
    # def create_superuser(self, username, email, password=None):
    #     user = self.create_user(username, email, password=password)
    #
    #     user.is_admin = True
    #     user.is_staff = True
    #     user.save(using=self._db)
    #     return user



class WebsiteSettings(models.Model):
    title = models.CharField(max_length=255)
    # favicon = models.ImageField(width_field=30, height_field=30)
    description = models.CharField(max_length=255)
    about = models.TextField(max_length=510)



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
