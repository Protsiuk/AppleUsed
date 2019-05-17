from django.db import models
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class MyUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, is_moderator, **extra_fields):
        """Creates and saves users with the given email and password"""
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, True, **extra_fields)

    def create_moderator(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, True, **extra_fields)


class MyCustomUser(AbstractUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(_('username'), max_length=254, unique=False, blank=True)
    email = models.EmailField(
        _('Email Address'), unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_moderator = models.BooleanField(_('moderator'), default=False)
    # appointment_moderator = models.DateTimeField(auto_now_add=False, auto_now=False)
    # fired_moderator = models.DateTimeField(auto_now_add=False, auto_now=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    birth_day = models.DateField(_('birthday'), blank=True, null=True)
    location_user = models.CharField(_('location'), default='', blank=True, null=True, max_length=512)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+9999999999'. Up to 15 digits allowed.")
    phone_number_user = models.CharField(_('Phone number user'), validators=[phone_regex], max_length=15, blank=True)  # validators should be a list

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyUserManager()

    class Meta:
        swappable = "AUTH_USER_MODEL"
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name


class WebsiteSettings(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    about = models.TextField(max_length=510)
