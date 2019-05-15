from django.db import models
from appleused_project import settings
from django.core.urlresolvers import reverse
from advertisements.models import Advertisement
from django.utils.translation import ugettext_lazy as _


class Checklist(models.Model):
    check_title = models.BooleanField(_('Checking of title'), default=False)
    check_description = models.BooleanField(_('Checking of description'), default=False)
    check_photos = models.BooleanField(_('Checking of photos'), default=False)

MODERATION_STATUS_REJECTED = 0
MODERATION_STATUS_APPROVED = 1
# MODERATION_STATUS_PENDING = 2
MODERATION_STATUS_AT_WORK = 2

STATUS_CHOICES = (
    (MODERATION_STATUS_REJECTED, 'rejected'),
    (MODERATION_STATUS_APPROVED, 'approved'),
    # (MODERATION_STATUS_PENDING, 'pending'),
    (MODERATION_STATUS_AT_WORK, 'at_work'),
)


class Moderation(models.Model):
    moderation_id = models.AutoField(primary_key=True)
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='moderator')
    ad_to_moderate = models.ForeignKey(Advertisement, null=True, on_delete=models.CASCADE, related_name='ad_to_moderate')
    time_sending_by_user = models.DateTimeField(_('Time sending ad by user for checking'), auto_now_add=False, auto_now=True)
    start_moderate = models.DateTimeField(_('Start checking'), auto_now_add=True, auto_now=False)
    end_moderate = models.DateTimeField(_('Finished checking'), auto_now_add=False, auto_now=True, null=True)
    comment_to_ad = models.CharField(_('Comment to advertisement'), max_length=255, default='', blank=True)
    status = models.SmallIntegerField(_('Choices status'), choices=STATUS_CHOICES, default=2)
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name='checklist', blank=True, null=True)

    class Meta:
        verbose_name = 'Moderation of advertisement'
        verbose_name_plural = 'Moderation of advertisements'

    def __str__(self):
        return 'Advertisement %s(ad-id: %s) moderate by %s' % (
            self.ad_to_moderate.title,
            self.ad_to_moderate.id,
            self.moderator
        )

    def get_absolute_url(self):
        return reverse("moderation:detail", kwargs={'pk': self.id})
