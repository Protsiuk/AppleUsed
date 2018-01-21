from django import forms
from django.contrib.auth import authenticate
from accounts.models import User
# from django.contrib.auth.models import User
# from accounts import


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

    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        return user


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
    eml = forms.EmailField()
    # password = forms.CharField(min_length=6, max_length=20, widget=forms.TextInput(attrs={"type": "password"}))

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


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=50)#(label=(u'Имя Пользователя'))
    email = forms.EmailField(max_length=50)#(label=(u'Email'))
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))#label=('Пароль'),
    passwordConfirm = forms.CharField(label=('Пароль повторно'), widget=forms.PasswordInput(render_value=False))

    # class Meta:
    #     model = user
    #     # Don't show user drop down.
    #     exclude = ('user',)


    def clean_email(self):
        email = self.cleaned_data['email']
        # if email:
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
                return email
        raise forms.ValidationError("Username already taken.")


    def clean(self):
        try:
            cleaned_data = super(RegistrationForm, self).clean()
            password = cleaned_data.get("password")
            passwordConfirm = cleaned_data.get('passwordConfirm')

            if password != passwordConfirm:
                raise forms.ValidationError("Password does not match, try again.")
            return cleaned_data
        except:
            raise forms.ValidationError("Error")


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