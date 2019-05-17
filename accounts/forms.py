from django import forms
from django.contrib.auth import authenticate
from accounts.models import MyCustomUser
from django.forms.widgets import SelectDateWidget
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=6, max_length=20, widget=forms.TextInput(attrs={"type": "password"}))

    def clean(self):
        data = self.cleaned_data
        user = authenticate(email=data.get("email"), password=data.get("password"))
        if not user:
            raise forms.ValidationError("Вы ввели некоректный email или пароль.")
        return self.cleaned_data

    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        return user

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=6, max_length=20, widget=forms.TextInput(attrs={"type": "password"}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError("Sorry, that login or password was invalid. Please try again.")
        return self.cleaned_data


class DateInput(forms.DateInput):
    input_type = 'date'


class UserRegistrationForm(forms.Form):

    first_name = forms.CharField(max_length=50)#(label=(u'Имя Пользователя')
    last_name = forms.CharField(max_length=50)  # (label=(u'Имя Пользователя')
    birthday = forms.DateField(widget=SelectDateWidget())
    email = forms.EmailField(max_length=50)#(label=(u'Email'), widget = forms.TextInput(attrs={'placeholder': 'Input email', 'class': 'form-control input-perso'}), max_length = 30, min_length = 3)
    password1 = forms.CharField(min_length=6, max_length=20, widget=forms.TextInput(attrs={"type": "password"}))
    password2 = forms.CharField(min_length=6, max_length=20, widget=forms.TextInput(attrs={"type": "password"}))

    class Meta:
        model = MyCustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'birthday',
            'password1',
            'password2'
            ]

        widgets = {'birthday': DateInput()}

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            MyCustomUser.objects.get(email=email)
        except MyCustomUser.DoesNotExist:
            return email
        raise forms.ValidationError("Данный Email уже есть в базе данных. "
                                    "Попробуйте использовать другой Email или пройдите процедуру востановления пароля.")

    def clean(self):
        try:
            cleaned_data = super(UserRegistrationForm, self).clean()
            password = cleaned_data.get("password")
            passwordConfirm = cleaned_data.get('passwordConfirm')
            if password != passwordConfirm:
                raise forms.ValidationError("Пароли не совпадают.")
            return cleaned_data
        except ValueError:
            raise forms.ValidationError("Error. Пожалуйста проверте еще раз данные")

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['First name']
        user.last_name = self.cleaned_data['Last name']

        if commit:
            user.save()
        return user


class CustomUserUpdateForm():
    first_name = forms.CharField(max_length=50)#(label=(u'Имя Пользователя')
    last_name = forms.CharField(max_length=50)  # (label=(u'Имя Пользователя')
    email = forms.EmailField(max_length=50)#(label=(u'Email'), widget = forms.TextInput(attrs={'placeholder': 'Input email', 'class': 'form-control input-perso'}), max_length = 30, min_length = 3)
    location_user = forms.CharField(max_length=150)

    class Meta:
        model = MyCustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'birth_day'
            'location_user',
            'password1',
            'password2'
            ]
        widgets = {'birth_day': DateInput(), }


class ProfileUserForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    birthday = forms.DateField(label='Birthday')
    location = forms.CharField(label='location', max_length=512)
    phone = forms.IntegerField(label='Phone')

    class Meta:
        user = MyCustomUser
        fields = '__all__'


class EditProfileUserForm(forms.ModelForm):
    """ form for updating users
    the field you want to use should already be defined in the model
    so no need to add them here again DRY"""

    class Meta:
        user = MyCustomUser
        fields = (
            'first_name',
            'last-name',
            'username',
            'birth_day',
            'location_user',
            'phone_number_user',
        )



class MyCustomUserCreationForm(UserCreationForm):
# class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    birth_day = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = MyCustomUser
        fields = ('username', 'email', 'password1', 'password2', 'birth_day')
