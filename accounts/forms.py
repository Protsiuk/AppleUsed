from django import forms
from django.contrib.auth import authenticate
from django.forms import ModelForm, modelformset_factory
from accounts.models import User, UserProfile

# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm#, UserCreationForm

# from registration.forms import RegistrationForm


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=6, max_length=20, widget=forms.TextInput(attrs={"type": "password"}))
    # password = forms.CharField(widget=forms.FilePathField, required=True)

    def clean(self):
        data = self.cleaned_data
        # email = self.cleaned_data.get('email')
        # password = self.cleaned_data.get('password')
        # user = authenticate(email=email, password=password)
        user = authenticate(email=data.get("email"), password=data.get("password"))
        if not user:
            raise forms.ValidationError("Вы ввели некоректный email или пароль.")
            # raise forms.ValidationError("Sorry, that login or password was invalid. Please try again.")
        return self.cleaned_data

    def login(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        return user


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=6, max_length=20, widget=forms.TextInput(attrs={"type": "password"}))

    # password = forms.CharField(widget=forms.FilePathField, required=True)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError("Sorry, that login or password was invalid. Please try again.")
        return self.cleaned_data


    # def clean(self):
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get('password')
    #     try:
    #         user = User.objects.get(email = email)
    #         if not user.is_active:
    #             raise forms.ValidationError("Email has not active. Try again.")
    #         else:
    #             return email
    #     except User.DoesNotExist:
    #         raise forms.ValidationError("User not Exist!")


        # user = authenticate(username='email', password='password')
        # print(user)

        # if len(email) < 14:
        #     raise forms.ValidationError("Sorry. Please try again.")
        # return self.cleaned_data
    # password = forms.CharField(min_length=10, max_length=20, widget=forms.TextInput(atr={"class": "password"}))


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(
        attrs={'placeholder': 'Имя пользователя', 'class': 'form-control input-data'}), max_length=50, min_length=3)
    email = forms.EmailField(label=u"Email", widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'class': 'form-control input-data'}), max_length=50, min_length=6)
    password = forms.CharField(label=u"Пароль", widget=forms.TextInput(
        attrs={'type': 'password', 'placeholder': 'Пароль', 'class': 'form-control input-data'}),
                               max_length=50, min_length=6)
    passwordConfirm = forms.CharField(label=u"Пароль", widget=forms.TextInput(
        attrs={'type': 'password', 'placeholder': 'Повторите пароль', 'class': 'form-control input-data'}),
                                      max_length=50, min_length=6)

    # passwordConfirm = forms.CharField(min_length=6, max_length=20, widget=forms.TextInput(attrs={"type": "password"}))

    # passwordConfirm = forms.CharField(label="", max_length=50, min_length=6,
    #                                   widget=forms.PasswordInput(attrs={'placeholder': 'Пароль повторно',
    #                                                               'class':'form-control input-perso'}))

        # (label=('Пароль повторно'), widget=forms.PasswordInput(render_value=False))
    class Meta:
        model = User
        # fields = (
        # #     'first_name',
        # #     'last_name',
        #     'last_name',
        #     'email',
        #     'password1',
        #     'password2'
        # )

    # class Meta:
    #     model = user
    #     # Don't show user drop down.
    #     exclude = ('user',)

    # def create_user(self, email=None, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', False)
    #     extra_fields.setdefault('is_superuser', False)
    #     return self._create_user(email, password, **extra_fields)


    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("Данный Email уже есть в нашей базе."
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
        # user.first_name = self.cleaned_data['First name']
        # user.last_name = self.cleaned_data['Last name']

        if commit:
            user.save()
        return user


"""class RegistrationForm(forms.Form):
    username = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur','class':'form-control input-perso'}),max_length=30,min_length=3,validators=[isValidUsername, validators.validate_slug])
    email = forms.EmailField(label="",widget=forms.EmailInput(attrs={'placeholder': 'Email','class':'form-control input-perso'}),max_length=100,error_messages={'invalid': ("Email invalide.")},validators=[isValidEmail])
    password1 = forms.CharField(label="",max_length=50,min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe','class':'form-control input-perso'}))
    password2 = forms.CharField(label="",max_length=50,min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer mot de passe','class':'form-control input-perso'}))

    #recaptcha = ReCaptchaField()

    #Override clean method to check password match
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            self._errors['password2'] = ErrorList([u"Le mot de passe ne correspond pas."])

        return self.cleaned_data

    #Override of save method for saving both User and Profile objects
    def save(self, datas):
        u = User.objects.create_user(datas['username'],
                                     datas['email'],
                                     datas['password1'])
        u.is_active = False
        u.save()
        profile=Profile()
        profile.user=u
        profile.activation_key=datas['activation_key']
        profile.key_expires=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profile.save()
        return u

    #Sending activation email ------>>>!! Warning : Domain name is hardcoded below !!<<<------
    #The email is written in a text file (it contains templatetags which are populated by the method below)
    def sendEmail(self, datas):
        link="http://yourdomain.com/activate/"+datas['activation_key']
        c=Context({'activation_link':link,'username':datas['username']})
        f = open(MEDIA_ROOT+datas['email_path'], 'r')
        t = Template(f.read())
        f.close()
        message=t.render(c)
        #print unicode(message).encode('utf8')
        send_mail(datas['email_subject'], message, 'yourdomain <no-reply@yourdomain.com>', [datas['email']], fail_silently=False)
        """


# class RegistrationForm(forms.Form):
#     username = forms.CharField(label=(u'Имя Пользователя'))
#     email = forms.EmailField(label=(u'Email'))
#     password = forms.CharField(label=(u'Пароль'), widget=forms.PasswordInput(render_value=False))
#     passwordConfirm = forms.CharField(label=(u'Пароль повторно'), widget=forms.PasswordInput(render_value=False))
#
#     class Meta:
#         model = user
#         # Don't show user drop down.
#         exclude = ('user',)
#
#
#     def clean_username(self):
#         username = self.cleaned_data['username']
#         try:
#                 User.objects.get(username=username)
#         except User.DoesNotExist:
#                 return username
#         raise forms.ValidationError("Username already taken.")
#
#
#     def clean(self):
#         try:
#             cleaned_data = super(RegistrationForm, self).clean()
#             password = cleaned_data.get("password")
#             passwordConfirm = cleaned_data.get('passwordConfirm')
#
#             if password != passwordConfirm:
#                 raise forms.ValidationError("Password does not match, try again.")
#             return cleaned_data
#         except:
#             raise forms.ValidationError("Error")
"""
class UserProfileForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    # password = forms.CharField(widget=forms.PasswordInput(render_value=False))#label=('Пароль'),
    # passwordConfirm = forms.CharField(label=('Пароль повторно'), widget=forms.PasswordInput(render_value=False))
    city = forms.CharField(label='location', max_length=350)
    phone = forms.IntegerField(label='Phone')
"""

class UserProfileForm(forms.ModelForm):
    class Meta:
            model = UserProfile
            # fields = ['user', 'first_name', 'last_name', 'phone', 'city']
            fields = ['user', 'phone', 'city']

    def save(self, user=None):
        user_profile = super(UserProfileForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile

# class EditProfileForm(forms.ModelForm):
#
#     first_name = forms.CharField(label='First Name')
#     last_name = forms.CharField(label='Last Name')
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name']


# class EditProfileUserForm(forms.ModelForm):
#     username = forms.CharField(max_length=50)
#     email = forms.EmailField(max_length=50)
#     first_name = forms.CharField(label='First Name')
#     last_name = forms.CharField(label='Last Name')
#     city = forms.CharField(label='location', max_length=350)
#     phone = forms.IntegerField(label='Phone')
#
#     class Meta:
#         user = User
#         fields =[
#             'email',
#             # 'birth_day',
#             'first_name',
#             'last-name',
#             'city',
#             'phone'
#         ]


        # field = (
        #     'email',
        #     # 'birth_day',
        #     'first_name',
        #     'last-name',
        #     'city',
        #     'phone'
        # )

#--------------------------------------------------------------
# class UserRegistrationForm(RegistrationForm):
#     first_name = forms.CharField(max_length=30, label=("First name"))
#     last_name = forms.CharField(max_length=30, label=("Last name"))
#
#     class Meta:
#         model = User
#         fields = ("email", "first_name", "last_name")


#--------------------------------------------------------------
# class UserRegistrationForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, label=("First name"))
#     last_name = forms.CharField(max_length=30, label=("Last name"))
#
#     class Meta:
#         model = User
#         fields = ("email", "first_name", "last_name")


class EditProfileUserForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    # modelformset_factory

    # username = forms.CharField(max_length=50)
    # email = forms.EmailField(max_length=50)
    # first_name = forms.CharField(label='First Name')
    # last_name = forms.CharField(label='Last Name')
    # city = forms.CharField(label='location', max_length=350)
    # phone = forms.IntegerField(label='Phone')

    # username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(
    #     attrs={'placeholder': 'Имя пользователя', 'class': 'form-control input-data'}), max_length=50, min_length=3)
    # email = forms.EmailField(label=u"Email", widget=forms.TextInput(
    #     attrs={'placeholder': 'Email', 'class': 'form-control input-data'}), max_length=50, min_length=6)
    # password = forms.CharField(label=u"Пароль", widget=forms.TextInput(
    #     attrs={'type': 'password', 'placeholder': 'Пароль', 'class': 'form-control input-data'}), max_length=50, min_length=6)
    # passwordConfirm = forms.CharField(label=u"Пароль", widget=forms.TextInput(
    #     attrs={'type': 'password', 'placeholder': 'Повторите пароль', 'class': 'form-control input-data'}), max_length=50, min_length=6)


    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, commit=True):
        user = super(EditProfileUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user