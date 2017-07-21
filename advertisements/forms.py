from django import forms


class AdvertisementForm(forms.Form):
    title = forms.CharField()
    price = forms.CharField()
    body = forms.CharField(widget=forms.Textarea())
    image = forms.FileField()


class AdvertisementFilterForm(forms.Form):
    min_price = forms.IntegerField(label='от', required=False)
    max_price = forms.IntegerField(label='до', required=False)
    # from_town = forms.CharField(max_length=100)
    # ordering = forms.ChoiceField(label='Сортировать по:', required=False, choices=[
    #     ['added', 'самые новые'],
    #     ['expensive', 'от дорогих к дешовым'],
    #     ['inexpensive', 'от дешовых к дорогим']])


class AdvertisementMessageForm(forms.Form):
    email_visitor = forms.EmailField(max_length=50)
    text = forms.CharField(widget=forms.Textarea())

