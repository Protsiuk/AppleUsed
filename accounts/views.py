from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.core.urlresolvers import reverse
# from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from password_reset import

# from accounts.serializers import LoginSerializer
from accounts.forms import LoginForm, RegistrationForm, ProfileUserForm, EditProfileUserForm#, ForgotPasswordForm

from accounts.models import User


def main_page(request):
    return render(request, "main.html")


# @login_required(login_url="/login/")
def sign_out(request):
    logout(request)
    return render(request, "main.html")
    # return HttpResponseRedirect(reverse("main"))


def sign_in(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("advertisements"))
    else:
        form = LoginForm(request.POST or None)
        if request.POST and form.is_valid():
            user = form.login(request)
            # print(request)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("advertisements"))
    return render(request, 'login.html', {'form': form})


def forgotPassword(request):
    form = LoginForm(request.GET)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("advertisements"))
    return render(request, 'login.html', {'form': form})


# class PasswordResetView():
#     print('сброс пароля')
#     form = ForgotPasswordForm
#     return render(request, 'password_reset.html', {'form': form})


"""
    form = LoginForm(request.POST or None)
    data = form.cleaned_data
    user = authenticate(email=data.get("email"), password=data.get("password"))
    # user = authenticate(email=data.get("email"), password=data.get("password"))
    if user is not None:
        print("user is authenticate", data.get("email"))
    else:
        raise forms.ValidationError("Sorry, that login or password was invalid. Please try again.")
    return render(request, "login.html", {"form": form})
"""


"""
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("main"))
    else:
        form = LoginForm()
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user = authenticate(email=data.get("email"), password=data.get("password"))
                if user:
                    login(request, user)
                    return HttpResponseRedirect(reverse("main"))
                # else:
                #     raise forms.ValidationError("Sorry, that login or password was invalid. Please try again.")
        return render(request, "login.html", {"form": form})
"""

        # # form = LoginForm()
        # form = LoginForm(request.POST)
        # if request.POST and form.is_valid:
        #     # form = LoginForm(request.POST)
        #     data = form.cleaned_data
        #     user = authenticate(email=data.get("email"), password=data.get("password"))
        #     if user:
        #         login(request, user)
        #         return render(request, "login.html", {"form": form})
        #         # return HttpResponseRedirect(reverse("main"))

        # if request.method == "POST":
        #     form = LoginForm(request.POST)
        #     if form.is_valid():
        #         data = form.cleaned_data
        #         user = authenticate(email=data.get("email"), password=data.get("password"))
        #         if not user:
        #             raise forms.ValidationError("Sorry, that login or password was invalid. Please try again.")
        #         else:
        #             login(request, user)
        #             return HttpResponseRedirect(reverse("main"))

                #     print(form.errors)

                    # raise ValidationError("Sorry, that login or password was invalid. Please try again.")
                    # print("sorry")
        # return render(request, "login.html", {"form": form})

"""
class UserLoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if Token.objects.filter(user=serializer.validated_data["user"]).exists():
                token = Token.objects.get(user=serializer.validated_data["user"])
            else:
                token = Token.objects.create(user=serializer.validated_data["user"])
            return Response({"success": True,
                             "token": token.key})
        else:
            return Response(serializer.errors)
"""
#
# @login_required
# def personal_details(request):
#     user = User.objects.get(pk=request.user.id)
#     profile = UserProfile.objects.get(user_id=request.user.id)
#     return render(request, 'personaldetails.html', {'profile': profile,'user':user})


# @login(request=GET, user=User.is_authenticated)
# @login_required(redirect_field_name='my_redirect_field')


# @login_required(login_url="/advertisements/")
# @should_be_anonymous(redirect_url=reverse_lazy('office'))
def registrationView(request):
    # if User.is_authenticated:
    form = RegistrationForm(request.POST or None)
    if request.user.is_anonymous() and request.POST:
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'])
            # print(user.objects.get['email'])
            user.save()
            # user = User.objects.get()
            return HttpResponseRedirect(reverse("profile_user"))
    return render(request, 'registration.html', {'form': form})
    # return HttpResponseRedirect(reverse('profile_user'))
"""
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('profile_user'))
    elif request.POST:
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'])
            # print(user.objects.get['email'])
            user.save()
            # user = User.objects.get()
            return HttpResponseRedirect(reverse("profile_user"))
    return render(request, 'registration.html', {'form': form})
"""

@login_required
def profileUserViews(request):
    # user = request.user
    # if request.GET:
    #     return user
    return render(request, 'profile-user.html', {'user': request.user})


# @login_required
# def editProfileUserViews(request):
#     user = request.user
#     if request.POST:
#         form = ProfileUserForm(request.POST)
#         user = User.objects.update(first_name=form.cleaned_data['first_name'],
#                                    last_name=form.cleaned_data['last_name'],
#                                    # phone=form.cleaned_data['last_name'],
#                                    city=form.cleaned_data['city'],
#                                             email=form.cleaned_data['email'],
#                                             password=form.cleaned_data['password'])
#     return render(request, 'edit-profile-user.html', {'form': form})


@login_required
def editProfileUserViews(request):
    # user = request.user
    if request.POST:
        form = EditProfileUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile-user.html'))
        # return render(request, 'profile-user.html', {'user': user})
    else:
        form = UserChangeForm(instance=request.user)
        return render(request, 'edit-profile-user.html', {'form' : form})
        # return redirect(reverse("edit-profile-user"))

    # return render(request, 'edit-profile-user.html', {'form': form})


# def create_profile(sender, **kwargs):
#     if kwargs['created']:
#         user_profile = UserProfile.objects.create(user=kwargs['instance'])


# post_save.connnect(create_profile, sender=User)