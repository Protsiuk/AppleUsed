from django import forms
from advertisements.models import Advertisement, AdvertisementImage
from betterforms.multiform import MultiModelForm


class AdvertisementForm(forms.ModelForm):
    # title = forms.CharField()
    # price = forms.CharField()
    # body = forms.CharField(widget=forms.Textarea())
    image = forms.FileField(label=u'Фотографии', widget=forms.FileInput(attrs={'multiple': 'multiple'}))

    class Meta:
        model = Advertisement
        fields = (
            # 'id',
            'title',
            'category_equipment',
            'price',
            'product_number',
            'phone_author',
            'description',
            'location_author',
        )


class AdvertisemenImageForm(forms.ModelForm):
    main_image = forms.BooleanField()
    class Meta:
        model = AdvertisementImage
        fields = (
            'image',
            'main_image'
            )


class AdvertisementCreationMultiForm(MultiModelForm):
    form_classes = {
        'AdvertisemenImage': AdvertisemenImageForm,
        'Advertisement': AdvertisementForm,
    }


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
    class Meta:
        model = Advertisement
        fields = (
            'text',
            'email_visitor',
        )

