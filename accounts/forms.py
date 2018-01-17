from django import forms
from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
# from accounts import


class LoginForm(forms.Form):
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

    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        return user


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
