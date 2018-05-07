
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

# from django.core.exceptions import ValidationError

from django.shortcuts import render, HttpResponseRedirect, redirect#, HttpResponse
# from django.contrib.sites.shortcuts import get_current_site

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from password_reset import

# from accounts.serializers import LoginSerializer
from accounts.forms import LoginForm, UserRegistrationForm, EditProfileUserForm, ProfileUserForm#, , ForgotPasswordForm

from accounts.models import User
# from accounts import signals

#all imports of django registration----------------------------------------------
# from registration.backends.default.views import RegistrationView
# from registration.models import RegistrationProfile
# from registration import signals
# #-----------------------------

# from django.contrib.auth import get_user_model
# from django.contrib.sites.shortcuts import get_current_site
# from django.core import signing
# from django.template.loader import render_to_string
# from .views import ActivationView as BaseActivationView
# from accounts.views import RegistrationView as BaseRegistrationView
#
# REGISTRATION_SALT = getattr(settings, 'REGISTRATION_SALT', 'registration')
#-----------------------------


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
    form = UserRegistrationForm(request.POST or None)
    if request.user.is_anonymous() and request.POST:
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'])
            # print(user.objects.get['email'])
            user.save()
            # user = User.objects.get()
            # return HttpResponseRedirect(reverse("profile_user"))
            return HttpResponseRedirect(reverse("advertisements"))
    return render(request, 'registration.html', {'form': form})
    # return HttpResponseRedirect(reverse('profile_user'))


def emailVerificationVellDonView(request):
    if request.POST:
        form = UserRegistrationForm(request.POST)
        # email visitor
        email_from = settings.EMAIL_HOST_USER
        email_to = form.cleaned_data['email']
        subject = "Verifikation email"
        massage_email = form.cleaned_data['text']
        # email_author = advertisement.author.email
        send_mail(subject, "Data sent: %s %s" % (subject, massage_email),
                  email_from,
                  [email_to],
                  fail_silently=True)
        return render(request, 'login.html', {'form': form})


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
        return render(request, 'edit-profile-user.html', {'form': form})
        # return redirect(reverse("edit-profile-user"))

    # return render(request, 'edit-profile-user.html', {'form': form})

# def create_profile(sender, **kwargs):
#     if kwargs['created']:
#         user_profile = UserProfile.objects.create(user=kwargs['instance'])


# post_save.connect(create_profile, sender=User)



# ----------------------------------------------------------------------------

"""
class RegistrationView(BaseRegistrationView):
"""    """
    Register a new (inactive) user account, generate an activation key
    and email it to the user.

    This is different from the model-based activation workflow in that
    the activation key is the username, signed using Django's
    TimestampSigner, with HMAC verification on activation.

"""    """
    email_body_template = 'registration/activation_email.txt'
    email_subject_template = 'registration/activation_email_subject.txt'

    def register(self, form):
        new_user = self.create_inactive_user(form)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=self.request)
        return new_user

    def get_success_url(self, user):
        return ('registration_complete', (), {})

    def create_inactive_user(self, form):
"""        """
        Create the inactive user account and send an email containing
        activation instructions.

"""        """
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.save()

        self.send_activation_email(new_user)

        return new_user

    def get_activation_key(self, user):
"""        """
        Generate the activation key which will be emailed to the user.

"""        """
        return signing.dumps(
            obj=getattr(user, user.USERNAME_FIELD),
            salt=REGISTRATION_SALT
        )

    def get_email_context(self, activation_key):
"""        """
        Build the template context used for the activation email.

"""        """
        scheme = 'https' if self.request.is_secure else 'http'
        return {
            'scheme': scheme,
            'activation_key': activation_key,
            'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
            'site': get_current_site(self.request)
        }

    def send_activation_email(self, user):
"""        """
        Send the activation email. The activation key is the username,
        signed using TimestampSigner.

"""        """
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context.update({
            'user': user,
        })
        subject = render_to_string(self.email_subject_template,
                                   context)
        # Force subject to a single line to avoid header-injection
        # issues.
        subject = ''.join(subject.splitlines())
        message = render_to_string(self.email_body_template,
                                   context)
        user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)


class ActivationView(BaseActivationView):
"""    """
    Given a valid activation key, activate the user's
    account. Otherwise, show an error message stating the account
    couldn't be activated.

"""    """
    success_url = 'registration_activation_complete'

    def activate(self, *args, **kwargs):
        # This is safe even if, somehow, there's no activation key,
        # because unsign() will raise BadSignature rather than
        # TypeError on a value of None.
        username = self.validate_key(kwargs.get('activation_key'))
        if username is not None:
            user = self.get_user(username)
            if user is not None:
                user.is_active = True
                user.save()
                return user
        return False

    def validate_key(self, activation_key):
"""        """
        Verify that the activation key is valid and within the
        permitted activation time window, returning the username if
        valid or ``None`` if not.

"""        """
        try:
            username = signing.loads(
                activation_key,
                salt=REGISTRATION_SALT,
                max_age=settings.ACCOUNT_ACTIVATION_DAYS * 86400
            )
            return username
        # SignatureExpired is a subclass of BadSignature, so this will
        # catch either one.
        except signing.BadSignature:
            return None

    def get_user(self, email):
"""        """
        Given the verified username, look up and return the
        corresponding user account if it exists, or ``None`` if it
        doesn't.
"""        """
        User = get_user_model()
        try:
            user = User.objects.get(**{
                User.USERNAME_FIELD: email,
                'is_active': False
            })
            return user
        except User.DoesNotExist:
            return None
"""

# this view fo django-registrtion -------------------------------------------------------------------

# class UserRegistrationView(RegistrationView):
#     form_class = UserRegistrationForm
#
#     def register(self, request, form):
#         if request == "POST":
#
#             site = get_current_site(request)
#
#             if hasattr(form, 'save'):
#                 new_user_instance = form.save()
#             else:
#                 new_user_instance = (User().objects
#                                      .create_user(**form.cleaned_data))
#
#             new_user = RegistrationProfile.objects.create_inactive_user(
#                 new_user=new_user_instance,
#                 site=site,
#                 send_email=self.SEND_ACTIVATION_EMAIL,
#                 request=request,
#             )
#         signals.user_registered.send(sender=self.__class__,
#                                      user=new_user,
#                                      request=request)
#         return new_user


#-------------------------------------------------------------------
"""
class UserRegistrationView():
    form_class = UserRegistrationForm

    def register(self, request, form):
        if request == "POST":
            site = get_current_site(request)

            if hasattr(form, 'save'):
                new_user_instance = form.save()
            else:
                new_user_instance = (User().objects.create_user(**form.cleaned_data))

            new_user = ProfileUserForm.objects.create_inactive_user(
                new_user=new_user_instance,
                site=site,
                send_email=self.SEND_ACTIVATION_EMAIL,
                request=request,
            )
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user
"""