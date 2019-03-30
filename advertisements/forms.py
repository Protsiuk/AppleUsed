from django import forms
from django.forms import inlineformset_factory
from advertisements.models import Advertisement, AdvertisementImage
from betterforms.multiform import MultiModelForm


class AdvertisementForm(forms.ModelForm):
    # title = forms.CharField()
    # price = forms.CharField()
    # body = forms.CharField(widget=forms.Textarea())
    # image = forms.FileField(label=u'Фотографии', widget=forms.FileInput(attrs={'multiple': 'multiple'}))

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
            'main_image'
        )


class AdvertisementImageForm(forms.ModelForm):
    class Meta:
        model = AdvertisementImage
        fields = [
            'image',
            ]

AdvertisementImageFormSet = inlineformset_factory(
    Advertisement,
    AdvertisementImage,
    extra=5,
    fields=('image',),
    can_delete=True
    )
    # form=AdvertisementImageForm,
    # fields=('image',))
    # extra=2)
    # widgets={'name': Textarea(attrs={'cols': 80, 'rows': 20})})#fields=('image',),


# class AdvertisementCreationMultiForm(MultiModelForm):
#     form_classes = {
#         'AdvertisementImageForm': AdvertisementImageForm,
#         'Advertisement': AdvertisementForm,
#     }


class AdvertisementMessageForm(forms.Form):
    email_visitor = forms.EmailField(max_length=50)
    text = forms.CharField(widget=forms.Textarea())
    class Meta:
        model = Advertisement
        fields = (
            'text',
            'email_visitor',
        )

class AdvertisementsSearchForm(forms.Form):
    q = forms.CharField(label="пошук", required=False)


class AdvertisementFilterForm(forms.Form):
    min_price = forms.IntegerField(label="от", required=False)
    max_price = forms.IntegerField(label="до", required=False)

    # from_town = forms.CharField(max_length=100)
    # ordering = forms.ChoiceField(label="Сортировка:", required=False, choices=[
    #     ["-added", "самые новые"],
    #     ["price", "по возрастанию цены"],
    #     ["-price", "по убыванию цены"]])

class AdvertisementsSearchFilterMultiForm(MultiModelForm):
    form_classes = {
        'AdvertisementsSearchForm': AdvertisementsSearchForm,
        'FilterForm': AdvertisementFilterForm,
    }
