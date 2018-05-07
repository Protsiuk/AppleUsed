from django import forms
# from advertisements.models import Advertisement
# from django.forms import ModelForm


class AdvertisementForm(forms.Form):
    title = forms.CharField()
    type_equipment = forms.CharField()
    price = forms.IntegerField()
    body = forms.CharField(widget=forms.Textarea())
    image = forms.ImageField()
    phone_author = forms.IntegerField()


    # author = forms.ForeignKey(User)

    # class Meta:
    #     model = Advertisement
    #     fields = '__all__'


class AdvertisementFilterForm(forms.Form):
    min_price = forms.IntegerField(label="от", required=False)
    max_price = forms.IntegerField(label="до", required=False)
    ordering = forms.ChoiceField(label='Сортировать', required=False, choices=[
        ['-added', 'самые новые'],
        ['-price', 'по возрастанию цены'],
        ['price', 'по убыванию цены'],
    ])
    # from_town = forms.CharField(max_length=100)
    # ordering = forms.ChoiceField(label='сортування', required=False, choices=[
    #     ['title', 'по алфавіту'],
    #     ['price', 'від найдешевших'],
    #     ['-price', 'від найдорожчих'],
    # ])


class AdvertisementMessageForm(forms.Form):
    email_visitor = forms.EmailField(max_length=50)
    text = forms.CharField(widget=forms.Textarea())
