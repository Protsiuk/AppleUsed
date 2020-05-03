from django.db import models
from django.db.models import Q
from AppleUsed import settings
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from utils import get_file_path
from solo.models import SingletonModel
from django.utils.translation import ugettext_lazy as _


class AdvertisementManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query)|
                         Q(description__icontains=query)|
                         Q(id__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


class Advertisement(models.Model):
    PC = 'iMac'
    NOTEBOOK = 'MacBook'
    TABLES = 'iPad'
    MONOBLOK = 'Monoblok'
    IPHONE = 'iPhone'
    MEDIAPLAYER = 'iPod'
    TV = 'MeidaBox'
    WATCH = 'Apple Watch'
    ACCESSORY = 'Accessory'
    CATEGORY_CHOICES = (
        (PC, 'iMac'),
        (NOTEBOOK, 'MacBook'),
        (TABLES, 'iPad'),
        (MONOBLOK, 'Monoblok'),
        (IPHONE, 'iPhone'),
        (MEDIAPLAYER, 'iPod'),
        (TV, 'MeidaBox'),
        (WATCH, 'Apple Watch'),
        (ACCESSORY, 'Accessory'),
        )
    title = models.CharField(_('Title advertisement'), max_length=255)
    category_equipment = models.CharField(_('Category advertisement'),
                                          max_length=25,
                                          choices=CATEGORY_CHOICES,
                                          default='iPhone'
                                          )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+9999999999'. Up to 15 digits allowed.")
    phone_author = models.CharField(_('Phone number author'), validators=[phone_regex], max_length=15, blank=True)
    description = models.TextField(_('Description advertisement'), default='')
    price = models.CharField(_('Price advertisement'), max_length=255)
    product_number = models.CharField(_('Manufacture/serial number'), max_length=25, blank=True, default='')
    slug = models.SlugField(_('slug'), blank=True, max_length=255)
    location_author = models.CharField(_('location'), default='', blank=True, max_length=512)
    main_image = models.ImageField(_('Main image advertisement'), upload_to=get_file_path, default='', blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_moderated = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=False)

    objects = AdvertisementManager()

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("advertisement:detail", kwargs={'slug': self.slug})

    # def set_is_visible(self):
    #     self.is_visible = True
    #     super(Advertisement).save()

    class Meta:
        verbose_name = 'Advertisement'
        verbose_name_plural = 'Advertisements'


class PageHit(models.Model):
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    advertisement = models.ForeignKey(Advertisement, null=True, on_delete=models.CASCADE, related_name='hits')
    hits_counter = models.PositiveIntegerField(_('Hit count'), default=0)

    def __str__(self):
        return 'Advertisement %s(ad-id: %s) has %s page hits' % (self.advertisement.title, self.advertisement.id, self.hits_counter)

    class Meta:
        verbose_name = 'Views of advertisement'
        verbose_name_plural = 'Views of advertisements'

    def advertisement_id(self):
        return self.advertisement.id


class AdvertisementFollowing (models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='follower')

    def __str__(self):
        return 'Follow user %s to %s (%s)' % (self.user.email, self.advertisement.title, self.advertisement.id)

    def get_ad_id(self):
        return self.advertisement.id

    def get_author_of_ad(self):
        return self.advertisement.author

    def get_absolute_url(self):
        return reverse("advertisement_detail", kwargs={'pk': self.advertisement.id})

    def get_api_favorite_url(self):
        return reverse("ad-api-favorite", kwargs={'pk': self.advertisement.id})

    class Meta:
        verbose_name = 'Advertisement is following'
        verbose_name_plural = 'Advertisements are following'


class AdvertisementImage(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, null=True, related_name='images')
    image = models.ImageField(_('Image advertisement'), upload_to=get_file_path, default='', blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % self.image

    class Meta:
        verbose_name = 'Image of Advertisement'
        verbose_name_plural = 'Images of Advertisements'


class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, default='Site name')
    maintenance_mode = models.BooleanField(default=False)

    def __unicode__(self):
        return u"Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
