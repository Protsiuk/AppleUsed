from django import forms


class AdvertisementForm(forms.Form):
    title = forms.CharField()
    price = forms.CharField()
    body = forms.CharField(widget=forms.Textarea())
    image = forms.FileField()


class AdvertisementMessageForm(forms.Form):
    email_visitor = forms.EmailField(max_length=50)
    text = forms.CharField(widget=forms.Textarea())

