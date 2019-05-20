from django import forms
from moderation.models import Moderation


class ModerationForm(forms.ModelForm):
    class Meta:
        model = Moderation
        fields = (
            'comment_to_ad',
            'status'
        )
