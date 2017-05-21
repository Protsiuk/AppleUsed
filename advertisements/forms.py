from django import forms


class AdvertisementForm(forms.Form):
    title = forms.CharField()
    price = forms.CharField()
    body = forms.CharField(widget=forms.Textarea())
    image = forms.FileField()


# class PublicationCommentForm(forms.Form):
#     text = forms.CharField(widget=forms.Textarea())