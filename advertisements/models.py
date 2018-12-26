from django.db import models
from appleused_project import settings
from django.core.validators import RegexValidator
from utils import get_file_path
from solo.models import SingletonModel
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin


class Advertisement(models.Model):
    PC = 'iMac'
    NOTEBOOK = 'MacBook'
    TABLES = 'iPad'
    MONOBLOK = 'Monoblok'
    IPHONE = 'iPhone'
    MEDIAPLAYER = 'iPod'
    TV = 'MeidaBox'
    WATCH = 'Apple Watch',
    CATEGORY_CHOICES = (
        (PC, 'iMac'),
        (NOTEBOOK, 'MacBook'),
        (TABLES, 'iPad'),
        (MONOBLOK, 'Monoblok'),
        (IPHONE, 'iPhone'),
        (MEDIAPLAYER, 'iPod'),
        (TV, 'MeidaBox'),
        (WATCH, 'Apple Watch'),
        )
    title = models.CharField(_('Title advertisment'), max_length=255)
    category_equipment = models.CharField(_('Category advertisment'),
                                          max_length=25,
                                          choices=CATEGORY_CHOICES,
                                          default='iPhone'
                                          )
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    # phone_author = models.CharField(_('Phone advertisment'), max_length=15)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+9999999999'. Up to 15 digits allowed.")
    phone_author = models.CharField(_('Phone number author'), validators=[phone_regex], max_length=15, blank=True)
    description = models.TextField(_('Description advertisment'), default='')
    # short_description = models.TextField(_('Short Description advertisment'), blank=True, null=False)
    price = models.CharField(_('Price advertisment'), max_length=255)
    # image = models.ImageField("фото", upload_to=get_file_path, default=None, blank=True)
    product_number = models.CharField(_('Manufacture/serial number'), max_length=25, blank=True, default='')
    slug = models.SlugField(_('slug'), blank=True, max_length=50)
    location_author = models.CharField(_('location'), default='', blank=True, max_length=512)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Advertisment'
        verbose_name_plural = 'Advertisments'

    # def
    # def get_images(self):
    #     return self.advertisementImage_set.all()

#     def get_views_count(self):
#         return PublicationLike.objects.filter(publication=self).count()
#
#
class AdvertisementFollowing (models.Model):
    advertisement = models.ForeignKey(Advertisement)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return 'Follow user %s to %s' % (self.user.email, self.advertisement.title)

    class Meta:
        verbose_name = 'Advertisment is following'
        verbose_name_plural = 'Advertisments are following'


class AdvertisementImage(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_('Image advertisment'), upload_to=get_file_path, default='', blank=True)
    main_image = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        # return 'Image %s of %s' % (self.image, self.advertisement.title)
        return '%s' % self.image

    class Meta:
        verbose_name = 'Image of Advertisment'
        verbose_name_plural = 'Images of Advertisments'


    # def get_object_qury(self):
    #     qs = []
    #     advertisement_with_photos =

class AdvertisementMessage (models.Model):
    advertisement = models.ForeignKey(Advertisement)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    email_visitor = models.EmailField(_('Email'), max_length=50)
    text = models.TextField(_('Text message'), max_length=500)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Massage %s  from %s to author - %s' % (self.email_visitor, self.text, self.author.email)

    class Meta:
        verbose_name = 'Advertisment massage'
        verbose_name_plural = 'Advertisment massages'


class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, default='Site name')
    maintenance_mode = models.BooleanField(default=False)

    def __unicode__(self):
        return u"Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
