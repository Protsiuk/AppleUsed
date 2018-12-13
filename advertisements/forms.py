from django import forms
from advertisements.models import Advertisement


class AdvertisementForm(forms.ModelForm):
    # title = forms.CharField()
    # price = forms.CharField()
    # body = forms.CharField(widget=forms.Textarea())
    # image = forms.FileField()

    class Meta:
        user = Advertisement
        fields = (
            'title',
            'category_equipment',
            'price',
            'phone_author',
            'description',
            'location_author',
            'phone_number_user',
        )


class AdvertisementFilterForm(forms.Form):
    min_price = forms.IntegerField(label="от", required=False)
    max_price = forms.IntegerField(label="до", required=False)
    # from_town = forms.CharField(max_length=100)
    # ordering = forms.ChoiceField(label="Сортировка:", required=False, choices=[
    #     ["-added", "самые новые"],
    #     ["price", "по возрастанию цены"],
    #     ["-price", "по убыванию цены"]])


class AdvertisementMessageForm(forms.Form):
    email_visitor = forms.EmailField(max_length=50)
    text = forms.CharField(widget=forms.Textarea())

