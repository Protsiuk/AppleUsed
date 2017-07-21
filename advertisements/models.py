from django.db import models
from accounts.models import User
from utils import get_file_path
from solo.models import SingletonModel


class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    type_equipment = models.CharField(max_length=255)
    phone_author = models.CharField(max_length=20)
    body = models.TextField()
    image = models.ImageField("фото", upload_to=get_file_path, default='', blank=True)
    # image = models.FileField(upload_to=get_file_path)
    author = models.ForeignKey(User)
    added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.id)


    # class Meta:
    #     ordering = ["-added"]


#     def get_views_count(self):
#         return PublicationLike.objects.filter(publication=self).count()
#
#
# class PublicationLike (models.Model):
#     publication = models.ForeignKey(Publication)
#     user = models.ForeignKey(User)


class AdvertisementMessage (models.Model):
    advertisement = models.ForeignKey(Advertisement, related_name="message")
    author = models.ForeignKey(User)
    email_visitor = models.EmailField(max_length=50)
    text = models.TextField()
    added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.text


class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, default='Site Name')
    maintenance_mode = models.BooleanField(default=False)

    def __unicode__(self):
        return u"Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
