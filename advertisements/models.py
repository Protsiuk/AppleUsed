from django.db import models
from appleused_project import settings
from django.core.validators import RegexValidator
from utils import get_file_path
from solo.models import SingletonModel
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin


class Advertisement(models.Model):
    PC = 'iMac'
    NOTEBOOK = 'MacBook'
    TABLES = 'iPad'
    MONOBLOK = 'Monoblok'
    IPHONE = 'iPhone'
    MEDIAPLAYER = 'iPod'
    TV = 'iPod'
    WATCH = 'Apple Watch',
    CATEGORY_CHOICES = (
        (PC, 'iMac'),
        (NOTEBOOK, 'MacBook'),
        (TABLES, 'iPad'),
        (MONOBLOK, 'Monoblok'),
        (IPHONE, 'iPhone'),
        (MEDIAPLAYER, 'iPod'),
        (TV, 'iPod'),
        (WATCH, 'Apple Watch'),
        )
    title = models.CharField(_('Title advertisment'), max_length=255)
    category_equipment = models.CharField(_('Category advertisment'),
                                          max_length=25,
                                          choices=CATEGORY_CHOICES,
                                          default='iPhone'
                                          )
    # phone_author = models.CharField(_('Phone advertisment'), max_length=15)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+9999999999'. Up to 15 digits allowed.")
    phone_author = models.CharField(_('Phone number author'), validators=[phone_regex], max_length=15, blank=True)
    description = models.TextField(_('Description advertisment'), null=False)
    # short_description = models.TextField(_('Short Description advertisment'), blank=True, null=False)
    price = models.CharField(_('Price advertisment'), max_length=255)
    # image = models.ImageField("фото", upload_to=get_file_path, default=None, blank=True)
    product_number = models.CharField(_('Manufacture/serial number'), max_length=25, blank=True, default='')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author')
    location_author = models.CharField(_('location'), default='', blank=True, null=True, max_length=512)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Advertisment'
        verbose_name_plural = 'Advertisments'


#     def get_views_count(self):
#         return PublicationLike.objects.filter(publication=self).count()
#
#
class AdvertisementFollowing (models.Model):
    advertisement = models.ForeignKey(Advertisement)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)


class AdvertisementImage(models.Model):
    advertisment = models.ForeignKey(Advertisement)
    image = models.ImageField(_('Image advertisment'), upload_to=get_file_path, default='', blank=True)
    main_image = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_active = models.BooleanField(default=True)


class AdvertisementMessage (models.Model):
    advertisement = models.ForeignKey(Advertisement, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    email_visitor = models.EmailField(_('Email'),max_length=50)
    text = models.TextField(_('Text message'), max_length=500)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, default='Site name')
    maintenance_mode = models.BooleanField(default=False)

    def __unicode__(self):
        return u"Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
