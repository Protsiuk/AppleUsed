# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy

from django.contrib.auth.tokens import default_token_generator

from django.shortcuts import render, HttpResponseRedirect, redirect, Http404, get_object_or_404#, HttpResponse
from django.contrib.sites.shortcuts import get_current_site


from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)


# from accounts.serializers import LoginSerializer
from accounts.forms import LoginForm, UserRegistrationForm, EditProfileUserForm, MyCustomUserCreationForm#, MyForm
# ProfileUserForm, ForgotPasswordForm

from accounts.models import MyCustomUser

# from accounts import signals
#---------------------------------------------------------CBV
from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout, get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView, ListView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import UpdateView, TemplateView
from django.contrib.auth.views import PasswordResetCompleteView

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

#
# def forgotPassword(request):
#     form = LoginForm(request.GET)
#     if request.POST and form.is_valid():
#         user = form.login(request)
#         if user:
#             auth_login(request, user)
#             return HttpResponseRedirect(reverse("advertisements"))
#     return render(request, 'login.html', {'form': form})


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


@login_required
def profileUserViews(request):
    user = request.user
    # print(user)
    if request.GET:
        return user
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


# @login_required
# def editProfileUserViews(request):
#     # user = request.user
#     if request.POST:
#         form = EditProfileUserForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('profile-user.html'))
#         # return render(request, 'profile-user.html', {'user': user})
#     else:
#         form = UserChangeForm(instance=request.user)
#         return render(request, 'edit-profile-user.html', {'form': form})
#         # return redirect(reverse("edit-profile-user"))
#
#     # return render(request, 'edit-profile-user.html', {'form': form})
#


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

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class UserProfileUpdateViews(LoginRequiredMixin, UpdateView):
    # form_class = EditProfileUserForm
    success_url = '/accounts/profile-user/'
    template_name = 'edit-profile-user.html'
    # queryset = MyCustomUser.objects.filter(user=request.user)
    """
    Base view for updating an existing object.
    Using this base class requires subclassing to provide a response mixin.
    """
    fields = ['username', 'first_name', 'last_name', 'birth_day', 'email', 'locations_user', 'phone_number_user']

    # def get(self):
    #     return MyCustomUser.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        return self.request.user

    # # @login_required
    # # def editProfileUserViews(self):
    # def edit(self):
    #     # user = request.user
    #     if self.request.POST:
    #         form = EditProfileUserForm(self.request.POST, instance=self.request.user)
    #         if form.is_valid():
    #             form.save()
    #             return redirect(reverse('profile-user.html'))
    #             # return render(request, 'profile-user.html', {'user': user})
    #     else:
    #         form = UserChangeForm(instance=self.request.user)
    #         return render(self.request, 'edit-profile-user.html', {'form': form})
    #
    #     """
    #     Base view for updating an existing object.
    #
    #     Using this base class requires subclassing to provide a response mixin.
    #     """
    #
    #     # def get(self, request, *args, **kwargs):
    #     #     self.object = self.get_object()
    #     #     return super(UserProfileUpdateViews, self).get(request, *args, **kwargs)
    #     #
    #     # def post(self, request, *args, **kwargs):
    #     #     self.object = self.get_object()
    #     #     return super(UserProfileUpdateViews, self).post(request, *args, **kwargs)


class MyProfileUser(DetailView):
    model = MyCustomUser
    template_name = 'profile-user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(request.user)
        context = self.get_context_data(object=self.object)
        # print(context)
        return self.render_to_response(context)

#--------- verification email

from django.http import HttpResponse
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetView
# from .forms import MyCustomUserCreationForm
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
        form = MyCustomUserCreationForm(request.POST)
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
        form = MyCustomUserCreationForm()
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
            print('token #1 is', str(token))
            print('INTERNAL_RESET_SESSION_TOKEN #2 is', str(INTERNAL_RESET_SESSION_TOKEN))
            print('INTERNAL_RESET_URL_TOKEN #2222 is', str(INTERNAL_RESET_URL_TOKEN))
            if token == INTERNAL_RESET_URL_TOKEN:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    # return super().dispatch(*args, **kwargs)
                    return super(MyUserPasswordResetConfirmView, self).dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    print('token #3 from session is', str(token))
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
        print('token #4 is', str(self.request.session[INTERNAL_RESET_SESSION_TOKEN]))
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



# _________________________________________________________________________________________________________________
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin

class SignUp(generic.CreateView):
    form_class = MyCustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

# class MyEdit(SuccessMessageMixin, UpdateView):
#     model = MyCustomUser
#     form_class = MyForm
#     template_name_suffix = '_edit'
#     success_message = '...'

#     title = _('Password reset complete')
#
#     def get_context_data(self, **kwargs):
#         context = super(PasswordResetCompleteView, self).get_context_data(**kwargs)
#         context['login_url'] = resolve_url(settings.LOGIN_URL)
#         return context




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
##
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
