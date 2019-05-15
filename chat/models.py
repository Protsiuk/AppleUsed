from django.db import models
# from django.contrib.auth.models import User

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from advertisements.models import Advertisement
from appleused_project import settings


class ChatManager(models.Manager):
    use_for_related_fields = True

    # if not user returned all of messages with unreaded status
    def unreaded(self, user=None):
        qs = self.get_queryset().exclude(last_send_message__isnull=True).filter(last_send_message__is_readed=False)
        return qs.exclude(last_send_message__author=user) if user else qs

    # def get_my_chats(self, user=None):
    #     pass

    # def get_last_message_in_chat(self):
    #     return self.filter(last_send_message__chat__in=)


class Chat(models.Model):
    DIALOG = 'D'
    MESSAGE_ = 'M'
    CHAT_TYPE_CHOICES = (
        (DIALOG, _('Dialog')),
        (MESSAGE_, _('Message'))
    )

    type = models.CharField(
        _('Type'),
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    # members = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("participants"))
    last_send_message = models.ForeignKey(
        'Message',
        related_name='last_send_message',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    objects = ChatManager()

    @models.permalink
    def get_absolute_url(self):
        return 'chat:dialog_list', (), {'chat_id': self.pk}

    # def get_members(self):
    #     return self.members

    # def get_last_message_in_chat(self):
    #     return self.objects.filter(last_send_message__chat__last_send_message=)


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name=_("Чат"), null=True)
    subject_ad = models.ForeignKey(Advertisement, verbose_name=_("Dialog about"))
    sender_msg = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sender'
    )
    receiver_msg = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='receiver'
    )
    temporary_user_email = models.EmailField(_('Temporary user'), blank=True, null=True)
    # author = models.ForeignKey(User, verbose_name=_("Пользователь"))
    message = models.TextField(_("Message"))
    pub_date = models.DateTimeField(_('Date of message'), auto_now_add=True, auto_now=False)
    is_readed = models.BooleanField(_('Was read'), default=False)
    reading_date = models.DateTimeField(_('Reading date'), auto_now_add=False, auto_now=False, null=True, blank=True)
    is_active = models.BooleanField(_('Was read'), default=True)

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return 'Message %s about %s' % (self.message[:50], self.subject_ad)

    # def set_reading_date(self):
    #     self.reading_date = timezone.now()
    #     return self.reading_date

    # def get_last_msg_in_chat(self):
    #     # return self.last_send_message.
    #     return self.objects.latest('pub_date')

    def get_sender_msg(self):
        return self.sender_msg

    def get_receiver_msg(self):
        return self.receiver_msg
