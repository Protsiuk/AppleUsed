# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy

from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)

# from django.core.exceptions import ValidationError

from django.shortcuts import render, HttpResponseRedirect, redirect#, HttpResponse
from django.contrib.sites.shortcuts import get_current_site

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from password_reset import

# from accounts.serializers import LoginSerializer
from accounts.forms import LoginForm, UserRegistrationForm, EditProfileUserForm # ProfileUserForm, , ForgotPasswordForm

from accounts.models import MyCustomUser
# from accounts import signals

#----------------------------------------------
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


@login_required(login_url="/login/")
def sign_out(request):
    logout(request)
    return render(request, "main.html")
    # return HttpResponseRedirect(reverse("main"))


def login_user(request):
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
            auth_login(request, user)
            return HttpResponseRedirect(reverse("advertisements"))
    return render(request, 'login.html', {'form': form})


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
            user = MyCustomUser.objects.create_user(username=form.cleaned_data['username'],
                                            email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'])
            # print(user.objects.get['email'])
            user.save()
            # user = User.objects.get()
            return HttpResponseRedirect(reverse("profile_user"))
    return render(request, 'registration.html', {'form': form})
    # return HttpResponseRedirect(reverse('profile_user'))

def emailVerificationVellDonView(request):
    if request.POST:
        form = UserRegistrationForm(request.POST)
        # email visitor
        email_from = settings.EMAIL_HOST_USER
        email_to = form.cleaned_data['email']
        subject = "Verification email"
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
#-------------------------------------------------------------------

# class UserRegistrationView(RegistrationView):
#     form_class = UserRegistrationForm
#
#     def register(self, request, form):
#
#         site = get_current_site(request)
#
#         if hasattr(form, 'save'):
#             new_user_instance = form.save()
#         else:
#             new_user_instance = (User().objects
#                                  .create_user(**form.cleaned_data))
#
#         new_user = RegistrationProfile.objects.create_inactive_user(
#             new_user=new_user_instance,
#             site=site,
#             send_email=self.SEND_ACTIVATION_EMAIL,
#             request=request,
#         )
#         signals.user_registered.send(sender=self.__class__,
#                                      user=new_user,
#                                      request=request)
#         return new_user

#------------------------------------------------------------------- Registration


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

class UserLoginView():
    pass

#---------------------------------------------------------CBV
from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout, get_user_model
# from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout, get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
from django.views.generic import UpdateView, TemplateView
from django.contrib.auth.views import PasswordResetCompleteView



class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = '/accounts/profile-user/'
    form_class = AuthenticationForm
    # form_class = LoginForm
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        # login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        # redirect_to = self.request.REQUEST.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/accounts/signin/'
    # url = '/advertisements/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class UserProfileUpdate(UpdateView):
    pass



#--------- verification email

from django.http import HttpResponse
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetView
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from accounts.tokens import account_activation_token
# from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            # mail_subject = 'Activate your blog account.'
            mail_subject = 'Активация акаунта.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            # return HttpResponse('Please confirm your email address to complete the registration')
            return HttpResponse(u'Пожалуйста подтвердите свой email. Инструкции отправлены на email')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        # user = User.objects.get(pk=uid)
        user = MyCustomUser.objects.get(pk=uid)
    # except(TypeError, ValueError, OverflowError, User.DoesNotExist):
    except(TypeError, ValueError, OverflowError, MyCustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        # login(request, user)
        # return redirect('home')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return HttpResponse(u'Спасибо, что присоеденились к нам. Теперь можeте использовать свои логин и пароль для авторизации')
    else:
        # return HttpResponse('Activation link is invalid!')
        return HttpResponse(u'Ссылка активации недействительна!')


# not worked yet
class RegisterView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = '/accounts/signin/'
    form_class = AuthenticationForm
    # form_class = LoginForm
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        # login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(RegisterView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        # redirect_to = self.request.REQUEST.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to

INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'
UserModel = get_user_model()
# ugettext_lazy = lazy(ugettext, six.text_type)


class MyUserPasswordResetConfirmView(PasswordResetConfirmView):
    # form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'
    title = _('Enter new password')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == INTERNAL_RESET_URL_TOKEN:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super(MyUserPasswordResetConfirmView, self).dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, INTERNAL_RESET_URL_TOKEN)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring on Python 3
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super(MyUserPasswordResetConfirmView, self).get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
            # login(self.request, user, self.post_reset_login_backend)
        return super(MyUserPasswordResetConfirmView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(MyUserPasswordResetConfirmView, self).get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('Password reset unsuccessful'),
                'validlink': False,
            })
        return context


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
    title = _('Password reset complete')

    def get_context_data(self, **kwargs):
        context = super(UserPasswordResetCompleteView, self).get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context


# #     template_name = 'registration/password_reset_complete.html'
# # class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
# class UserPasswordResetCompleteView(PasswordResetCompleteView):
#     template_name = 'registration/password_reset_complete.html'
#     title = _('Password reset complete')




#     title = _('Password reset complete')
#
#     def get_context_data(self, **kwargs):
#         context = super(PasswordResetCompleteView, self).get_context_data(**kwargs)
#         context['login_url'] = resolve_url(settings.LOGIN_URL)
#         return context




# import functools
# import warnings
#
# from django.conf import settings
# # Avoid shadowing the login() and logout() views below.
# from django.contrib.auth import (
#     REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
#     logout as auth_logout, update_session_auth_hash,
# )
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import (
#     AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
# )
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.sites.shortcuts import get_current_site
# from django.http import HttpResponseRedirect, QueryDict
# from django.shortcuts import resolve_url
# from django.template.response import TemplateResponse
# from django.urls import reverse, reverse_lazy
# from django.utils.decorators import method_decorator
# from django.utils.deprecation import (
#     RemovedInDjango20Warning, RemovedInDjango21Warning,
# )
# from django.utils.encoding import force_text
# from django.utils.http import is_safe_url, urlsafe_base64_decode
# from django.utils.six.moves.urllib.parse import urlparse, urlunparse
# from django.utils.translation import ugettext_lazy as _
# from django.views.decorators.cache import never_cache
# from django.views.decorators.csrf import csrf_protect
# from django.views.decorators.debug import sensitive_post_parameters
# from django.views.generic.base import TemplateView
# from django.views.generic.edit import FormView
#
# UserModel = get_user_model()
#
#
# def deprecate_current_app(func):
#     """
#     Handle deprecation of the current_app parameter of the views.
#     """
#     @functools.wraps(func)
#     def inner(*args, **kwargs):
#         if 'current_app' in kwargs:
#             warnings.warn(
#                 "Passing `current_app` as a keyword argument is deprecated. "
#                 "Instead the caller of `{0}` should set "
#                 "`request.current_app`.".format(func.__name__),
#                 RemovedInDjango20Warning
#             )
#             current_app = kwargs.pop('current_app')
#             request = kwargs.get('request', None)
#             if request and current_app is not None:
#                 request.current_app = current_app
#         return func(*args, **kwargs)
#     return inner
#
#
# class SuccessURLAllowedHostsMixin(object):
#     success_url_allowed_hosts = set()
#
#     def get_success_url_allowed_hosts(self):
#         allowed_hosts = {self.request.get_host()}
#         allowed_hosts.update(self.success_url_allowed_hosts)
#         return allowed_hosts
#
#
# class LoginView(SuccessURLAllowedHostsMixin, FormView):
#     """
#     Displays the login form and handles the login action.
#     """
#     form_class = AuthenticationForm
#     authentication_form = None
#     redirect_field_name = REDIRECT_FIELD_NAME
#     template_name = 'registration/login.html'
#     redirect_authenticated_user = False
#     extra_context = None
#
#     @method_decorator(sensitive_post_parameters())
#     @method_decorator(csrf_protect)
#     @method_decorator(never_cache)
#     def dispatch(self, request, *args, **kwargs):
#         if self.redirect_authenticated_user and self.request.user.is_authenticated:
#             redirect_to = self.get_success_url()
#             if redirect_to == self.request.path:
#                 raise ValueError(
#                     "Redirection loop for authenticated user detected. Check that "
#                     "your LOGIN_REDIRECT_URL doesn't point to a login page."
#                 )
#             return HttpResponseRedirect(redirect_to)
#         return super(LoginView, self).dispatch(request, *args, **kwargs)
#
#     def get_success_url(self):
#         url = self.get_redirect_url()
#         return url or resolve_url(settings.LOGIN_REDIRECT_URL)
#
#     def get_redirect_url(self):
#         """Return the user-originating redirect URL if it's safe."""
#         redirect_to = self.request.POST.get(
#             self.redirect_field_name,
#             self.request.GET.get(self.redirect_field_name, '')
#         )
#         url_is_safe = is_safe_url(
#             url=redirect_to,
#             allowed_hosts=self.get_success_url_allowed_hosts(),
#             require_https=self.request.is_secure(),
#         )
#         return redirect_to if url_is_safe else ''
#
#     def get_form_class(self):
#         return self.authentication_form or self.form_class
#
#     def get_form_kwargs(self):
#         kwargs = super(LoginView, self).get_form_kwargs()
#         kwargs['request'] = self.request
#         return kwargs
#
#     def form_valid(self, form):
#         """Security check complete. Log the user in."""
#         auth_login(self.request, form.get_user())
#         return HttpResponseRedirect(self.get_success_url())
#
#     def get_context_data(self, **kwargs):
#         context = super(LoginView, self).get_context_data(**kwargs)
#         current_site = get_current_site(self.request)
#         context.update({
#             self.redirect_field_name: self.get_redirect_url(),
#             'site': current_site,
#             'site_name': current_site.name,
#         })
#         if self.extra_context is not None:
#             context.update(self.extra_context)
#         return context
#
#
# # @deprecate_current_app
# # def login(request, template_name='registration/login.html',
# #           redirect_field_name=REDIRECT_FIELD_NAME,
# #           authentication_form=AuthenticationForm,
# #           extra_context=None, redirect_authenticated_user=False):
# #     warnings.warn(
# #         'The login() view is superseded by the class-based LoginView().',
# #         RemovedInDjango21Warning, stacklevel=2
# #     )
# #     return LoginView.as_view(
# #         template_name=template_name,
# #         redirect_field_name=redirect_field_name,
# #         form_class=authentication_form,
# #         extra_context=extra_context,
# #         redirect_authenticated_user=redirect_authenticated_user,
# #     )(request)
#
#
# class LogoutView(SuccessURLAllowedHostsMixin, TemplateView):
#     """
#     Logs out the user and displays 'You are logged out' message.
#     """
#     next_page = None
#     redirect_field_name = REDIRECT_FIELD_NAME
#     template_name = 'registration/logged_out.html'
#     extra_context = None
#
#     @method_decorator(never_cache)
#     def dispatch(self, request, *args, **kwargs):
#         auth_logout(request)
#         next_page = self.get_next_page()
#         if next_page:
#             # Redirect to this page until the session has been cleared.
#             return HttpResponseRedirect(next_page)
#         return super(LogoutView, self).dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         """Logout may be done via POST."""
#         return self.get(request, *args, **kwargs)
#
#     def get_next_page(self):
#         if self.next_page is not None:
#             next_page = resolve_url(self.next_page)
#         elif settings.LOGOUT_REDIRECT_URL:
#             next_page = resolve_url(settings.LOGOUT_REDIRECT_URL)
#         else:
#             next_page = self.next_page
#
#         if (self.redirect_field_name in self.request.POST or
#                 self.redirect_field_name in self.request.GET):
#             next_page = self.request.POST.get(
#                 self.redirect_field_name,
#                 self.request.GET.get(self.redirect_field_name)
#             )
#             url_is_safe = is_safe_url(
#                 url=next_page,
#                 allowed_hosts=self.get_success_url_allowed_hosts(),
#                 require_https=self.request.is_secure(),
#             )
#             # Security check -- Ensure the user-originating redirection URL is
#             # safe.
#             if not url_is_safe:
#                 next_page = self.request.path
#         return next_page
#
#     def get_context_data(self, **kwargs):
#         context = super(LogoutView, self).get_context_data(**kwargs)
#         current_site = get_current_site(self.request)
#         context.update({
#             'site': current_site,
#             'site_name': current_site.name,
#             'title': _('Logged out'),
#         })
#         if self.extra_context is not None:
#             context.update(self.extra_context)
#         return context
#
#
# @deprecate_current_app
# def logout_then_login(request, login_url=None, extra_context=_sentinel):
#     """
#     Logs out the user if they are logged in. Then redirects to the log-in page.
#     """
#     if extra_context is not _sentinel:
#         warnings.warn(
#             "The unused `extra_context` parameter to `logout_then_login` "
#             "is deprecated.", RemovedInDjango21Warning
#         )
#
#     if not login_url:
#         login_url = settings.LOGIN_URL
#     login_url = resolve_url(login_url)
#     return LogoutView.as_view(next_page=login_url)(request)
#
#
# def redirect_to_login(next, login_url=None,
#                       redirect_field_name=REDIRECT_FIELD_NAME):
#     """
#     Redirects the user to the login page, passing the given 'next' page
#     """
#     resolved_url = resolve_url(login_url or settings.LOGIN_URL)
#
#     login_url_parts = list(urlparse(resolved_url))
#     if redirect_field_name:
#         querystring = QueryDict(login_url_parts[4], mutable=True)
#         querystring[redirect_field_name] = next
#         login_url_parts[4] = querystring.urlencode(safe='/')
#
#     return HttpResponseRedirect(urlunparse(login_url_parts))
#
#
# # 4 views for password reset:
# # - password_reset sends the mail
# # - password_reset_done shows a success message for the above
# # - password_reset_confirm checks the link the user clicked and
# #   prompts for a new password
# # - password_reset_complete shows a success message for the above
#
# @deprecate_current_app
# @csrf_protect
# def password_reset(request,
#                    template_name='registration/password_reset_form.html',
#                    email_template_name='registration/password_reset_email.html',
#                    subject_template_name='registration/password_reset_subject.txt',
#                    password_reset_form=PasswordResetForm,
#                    token_generator=default_token_generator,
#                    post_reset_redirect=None,
#                    from_email=None,
#                    extra_context=None,
#                    html_email_template_name=None,
#                    extra_email_context=None):
#     warnings.warn("The password_reset() view is superseded by the "
#                   "class-based PasswordResetView().",
#                   RemovedInDjango21Warning, stacklevel=2)
#     if post_reset_redirect is None:
#         post_reset_redirect = reverse('password_reset_done')
#     else:
#         post_reset_redirect = resolve_url(post_reset_redirect)
#     if request.method == "POST":
#         form = password_reset_form(request.POST)
#         if form.is_valid():
#             opts = {
#                 'use_https': request.is_secure(),
#                 'token_generator': token_generator,
#                 'from_email': from_email,
#                 'email_template_name': email_template_name,
#                 'subject_template_name': subject_template_name,
#                 'request': request,
#                 'html_email_template_name': html_email_template_name,
#                 'extra_email_context': extra_email_context,
#             }
#             form.save(**opts)
#             return HttpResponseRedirect(post_reset_redirect)
#     else:
#         form = password_reset_form()
#     context = {
#         'form': form,
#         'title': _('Password reset'),
#     }
#     if extra_context is not None:
#         context.update(extra_context)
#
#     return TemplateResponse(request, template_name, context)
#
#
# @deprecate_current_app
# def password_reset_done(request,
#                         template_name='registration/password_reset_done.html',
#                         extra_context=None):
#     warnings.warn("The password_reset_done() view is superseded by the "
#                   "class-based PasswordResetDoneView().",
#                   RemovedInDjango21Warning, stacklevel=2)
#     context = {
#         'title': _('Password reset sent'),
#     }
#     if extra_context is not None:
#         context.update(extra_context)
#
#     return TemplateResponse(request, template_name, context)
#
#
# # Doesn't need csrf_protect since no-one can guess the URL
# @sensitive_post_parameters()
# @never_cache
# @deprecate_current_app
# def password_reset_confirm(request, uidb64=None, token=None,
#                            template_name='registration/password_reset_confirm.html',
#                            token_generator=default_token_generator,
#                            set_password_form=SetPasswordForm,
#                            post_reset_redirect=None,
#                            extra_context=None):
#     """
#     View that checks the hash in a password reset link and presents a
#     form for entering a new password.
#     """
#     warnings.warn("The password_reset_confirm() view is superseded by the "
#                   "class-based PasswordResetConfirmView().",
#                   RemovedInDjango21Warning, stacklevel=2)
#     assert uidb64 is not None and token is not None  # checked by URLconf
#     if post_reset_redirect is None:
#         post_reset_redirect = reverse('password_reset_complete')
#     else:
#         post_reset_redirect = resolve_url(post_reset_redirect)
#     try:
#         # urlsafe_base64_decode() decodes to bytestring on Python 3
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = UserModel._default_manager.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
#         user = None
#
#     if user is not None and token_generator.check_token(user, token):
#         validlink = True
#         title = _('Enter new password')
#         if request.method == 'POST':
#             form = set_password_form(user, request.POST)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponseRedirect(post_reset_redirect)
#         else:
#             form = set_password_form(user)
#     else:
#         validlink = False
#         form = None
#         title = _('Password reset unsuccessful')
#     context = {
#         'form': form,
#         'title': title,
#         'validlink': validlink,
#     }
#     if extra_context is not None:
#         context.update(extra_context)
#
#     return TemplateResponse(request, template_name, context)
#
#
# @deprecate_current_app
# def password_reset_complete(request,
#                             template_name='registration/password_reset_complete.html',
#                             extra_context=None):
#     warnings.warn("The password_reset_complete() view is superseded by the "
#                   "class-based PasswordResetCompleteView().",
#                   RemovedInDjango21Warning, stacklevel=2)
#     context = {
#         'login_url': resolve_url(settings.LOGIN_URL),
#         'title': _('Password reset complete'),
#     }
#     if extra_context is not None:
#         context.update(extra_context)
#
#     return TemplateResponse(request, template_name, context)


# # Class-based password reset views
# # - PasswordResetView sends the mail
# # - PasswordResetDoneView shows a success message for the above
# # - PasswordResetConfirmView checks the link the user clicked and
# #   prompts for a new password
# # - PasswordResetCompleteView shows a success message for the above
#
# class PasswordContextMixin(object):
#     extra_context = None
#
#     def get_context_data(self, **kwargs):
#         context = super(PasswordContextMixin, self).get_context_data(**kwargs)
#         context['title'] = self.title
#         if self.extra_context is not None:
#             context.update(self.extra_context)
#         return context
#
#
# class UserPasswordResetView(PasswordResetView):
#     # email_template_name = 'registration/password_reset_email.html'
#     # extra_email_context = None
#     # form_class = PasswordResetForm
#     # from_email = None
#     # html_email_template_name = None
#     subject_template_name = 'registration/password_reset_subject.txt'
#     success_url = reverse_lazy('password_reset_done')
#     template_name = 'registration/password_reset_form.html'
#     title = _('Password reset')
#     token_generator = default_token_generator
#
#     @method_decorator(csrf_protect)
#     def dispatch(self, *args, **kwargs):
#         return super(UserPasswordResetView, self).dispatch(*args, **kwargs)
#
#     def form_valid(self, form):
#         opts = {
#             'use_https': self.request.is_secure(),
#             'token_generator': self.token_generator,
#             'from_email': self.from_email,
#             'email_template_name': self.email_template_name,
#             'subject_template_name': self.subject_template_name,
#             'request': self.request,
#             'html_email_template_name': self.html_email_template_name,
#             'extra_email_context': self.extra_email_context,
#         }
#         form.save(**opts)
#         return super(UserPasswordResetView, self).form_valid(form)
# #
#
# INTERNAL_RESET_URL_TOKEN = 'set-password'
# INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'
#
#
# class PasswordResetDoneView(PasswordContextMixin, TemplateView):
#     template_name = 'registration/password_reset_done.html'
#     title = _('Password reset sent')
#
#
# class PasswordResetConfirmView(PasswordContextMixin, FormView):
#     form_class = SetPasswordForm
#     post_reset_login = False
#     post_reset_login_backend = None
#     success_url = reverse_lazy('password_reset_complete')
#     template_name = 'registration/password_reset_confirm.html'
#     title = _('Enter new password')
#     token_generator = default_token_generator
#
#     @method_decorator(sensitive_post_parameters())
#     @method_decorator(never_cache)
#     def dispatch(self, *args, **kwargs):
#         assert 'uidb64' in kwargs and 'token' in kwargs
#
#         self.validlink = False
#         self.user = self.get_user(kwargs['uidb64'])
#
#         if self.user is not None:
#             token = kwargs['token']
#             if token == INTERNAL_RESET_URL_TOKEN:
#                 session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
#                 if self.token_generator.check_token(self.user, session_token):
#                     # If the token is valid, display the password reset form.
#                     self.validlink = True
#                     return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)
#             else:
#                 if self.token_generator.check_token(self.user, token):
#                     # Store the token in the session and redirect to the
#                     # password reset form at a URL without the token. That
#                     # avoids the possibility of leaking the token in the
#                     # HTTP Referer header.
#                     self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
#                     redirect_url = self.request.path.replace(token, INTERNAL_RESET_URL_TOKEN)
#                     return HttpResponseRedirect(redirect_url)
#
#         # Display the "Password reset unsuccessful" page.
#         return self.render_to_response(self.get_context_data())
#
#     def get_user(self, uidb64):
#         try:
#             # urlsafe_base64_decode() decodes to bytestring on Python 3
#             uid = force_text(urlsafe_base64_decode(uidb64))
#             user = UserModel._default_manager.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
#             user = None
#         return user
#
#     def get_form_kwargs(self):
#         kwargs = super(PasswordResetConfirmView, self).get_form_kwargs()
#         kwargs['user'] = self.user
#         return kwargs
#
#     def form_valid(self, form):
#         user = form.save()
#         del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
#         if self.post_reset_login:
#             auth_login(self.request, user, self.post_reset_login_backend)
#         return super(PasswordResetConfirmView, self).form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super(PasswordResetConfirmView, self).get_context_data(**kwargs)
#         if self.validlink:
#             context['validlink'] = True
#         else:
#             context.update({
#                 'form': None,
#                 'title': _('Password reset unsuccessful'),
#                 'validlink': False,
#             })
#         return context
#
#
# class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
#     template_name = 'registration/password_reset_complete.html'
#     title = _('Password reset complete')
#
#     def get_context_data(self, **kwargs):
#         context = super(PasswordResetCompleteView, self).get_context_data(**kwargs)
#         context['login_url'] = resolve_url(settings.LOGIN_URL)
#         return context


# class PasswordChangeView(PasswordContextMixin, FormView):
#     form_class = PasswordChangeForm
#     success_url = reverse_lazy('password_change_done')
#     template_name = 'registration/password_change_form.html'
#     title = _('Password change')
#
#     @method_decorator(sensitive_post_parameters())
#     @method_decorator(csrf_protect)
#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(PasswordChangeView, self).dispatch(*args, **kwargs)
#
#     def get_form_kwargs(self):
#         kwargs = super(PasswordChangeView, self).get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs
#
#     def form_valid(self, form):
#         form.save()
#         # Updating the password logs out all other sessions for the user
#         # except the current one.
#         update_session_auth_hash(self.request, form.user)
#         return super(PasswordChangeView, self).form_valid(form)
#
#
# class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
#     template_name = 'registration/password_change_done.html'
#     title = _('Password change successful')
#
#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(PasswordChangeDoneView, self).dispatch(*args, **kwargs)
#
