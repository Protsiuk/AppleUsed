from django import forms
from captcha.fields import CaptchaField
from chat.models import Message


class UserMessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('message',)
        # widget = forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})


class GuestMessageForm(forms.ModelForm):
    captcha = CaptchaField(label='Bвeдитe текст с картинки', error_messages={'invalid': 'Неправильный текст'})

    class Meta:
        model = Message
        fields = (
            'temporary_user_email',
            'message',
        )
        # exclude = ('is_active',)
        # widgets = {'bb': forms.HiddenInput}
