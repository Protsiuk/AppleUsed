from django.db import models
from accounts.models import User
from utils import get_file_path
# from solo.models import SingletonModel


class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    type_equipment = models.CharField(max_length=255)
    phone_user = models.CharField(max_length=20)
    body = models.TextField()
    image = models.FileField(upload_to=get_file_path)
    author = models.ForeignKey(User)
    added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.id)


#     def get_views_count(self):
#         return PublicationLike.objects.filter(publication=self).count()
#
#
# class PublicationLike (models.Model):
#     publication = models.ForeignKey(Publication)
#     user = models.ForeignKey(User)



class AdvertisementMesage (models.Model):
    advertisement = models.ForeignKey(Advertisement, related_name="comments")
    user = models.ForeignKey(User)
    text = models.TextField()
    added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.text[:50]

#
# class SiteConfiguration(SingletonModel):
#     site_name = models.CharField(max_length=255, default='Site Name')
#     maintenance_mode = models.BooleanField(default=False)
#
#     def __unicode__(self):
#         return u"Site Configuration"
#
#     class Meta:
#         verbose_name = "Site Configuration"
