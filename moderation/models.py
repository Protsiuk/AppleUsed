from django.db import models
from appleused_project import settings
from django.core.urlresolvers import reverse
from utils import get_file_path
from advertisements.models import Advertisement
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class Moderator(models.Model):
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='moderator')
    appointment = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Moderator'
        verbose_name_plural = 'Moderators'

    def __str__(self):
        return 'Moderator is %s' % self.moderator.email

    @property
    def is_moderator(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated and is staff in templates.
        """
        return True


class Checklist(models.Model):
    check_title = models.BooleanField(_('Checking of title'), default=False)
    check_description = models.BooleanField(_('Checking of description'), default=False)
    check_photos = models.BooleanField(_('Checking of photos'), default=False)

MODERATION_STATUS_REJECTED = 0
MODERATION_STATUS_APPROVED = 1
MODERATION_STATUS_PENDING = 2
MODERATION_STATUS_AT_WORK = 3


# MODERATION_STATUS_REJECTED = 'rejected'
# MODERATION_STATUS_APPROVED = 'approved'
# MODERATION_STATUS_PENDING = 'pending'
# MODERATION_STATUS_AT_WORK = 'at_work'

STATUS_CHOICES = (
    (MODERATION_STATUS_REJECTED, 'rejected'),
    (MODERATION_STATUS_APPROVED, 'approved'),
    (MODERATION_STATUS_PENDING, 'pending'),
    (MODERATION_STATUS_AT_WORK, 'at_work'),
)


class Moderation(models.Model):

    moderator = models.ForeignKey(Moderator, on_delete=models.CASCADE)
    ad_to_moderate = models.ForeignKey(Advertisement, null=True, on_delete=models.CASCADE, related_name='ad_to_moderate')
    time_sending_by_user = models.DateTimeField(_('Time sending ad by user for checking'), auto_now_add=False, auto_now=True)
    start_moderate = models.DateTimeField(_('Start checking'), auto_now_add=True, auto_now=False)
    end_moderate = models.DateTimeField(_('Finished checking'), auto_now_add=False, auto_now=True)
    comment_to_ad = models.CharField(_('Comment to advertisement'), max_length=255, default='', blank=True)
    status = models.SmallIntegerField(_('Choices status'), choices=STATUS_CHOICES, default='pending')
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name='moderator')

    class Meta:
        verbose_name = 'Moderation of advertisement'
        verbose_name_plural = 'Moderation of advertisements'

    def __str__(self):
        return 'Advertisement %s(ad-id: %s) moderate by %s' % (self.ad_to_moderate.title, self.ad_to_moderate.id, self.moderator)

    # def get_absolute_url(self):
    #     return reverse("moderation:detail", kwargs={'pk': self.id})

    # def get_list_url(self):
    #     return reverse("moderation:detail", kwargs={'pk': self.id})

    # def spent_time_moderation(self):
    #     pass
