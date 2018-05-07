from django.db import models
from accounts.models import User
from utils import get_file_path
from solo.models import SingletonModel


class Advertisement(models.Model):
    title = models.CharField('Тема', max_length=255)
    price = models.IntegerField("цена")
    type_equipment = models.CharField('Тип оборудования', max_length=255)
    phone_author = models.IntegerField('Телефон автора')
    body = models.TextField('Текст объявления', max_length=500)
    image = models.ImageField('Фото', upload_to=get_file_path, null=True, blank=True)#height_field=640, width_field=480
    # image = models.FileField(upload_to=get_file_path)
    author = models.ForeignKey(User)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "advertisement"
        verbose_name_plural = "advertisements"
        ordering = ["-added"]

    def __str__(self):
        return str(self.title)

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
    author = models.ForeignKey(User, related_name="author")
    email_visitor = models.EmailField(max_length=50)
    text_massage = models.TextField("Сообщение", max_length=450, default='')
    added = models.DateTimeField(auto_now_add=True)
    # is_favorite = models.BooleanField(default=False)


    def __str__(self):
        return self.text_massage


class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, default='Site Name')
    maintenance_mode = models.BooleanField(default=False)

    def __unicode__(self):
        return u"Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
