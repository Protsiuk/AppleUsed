from django.conf.urls import url#, include

from accounts.views import login_user, registrationView, profileUserViews, UserProfileUpdateViews,\
    LoginView, LogoutView, signup, SignUp, activate, MyUserPasswordResetConfirmView, UserPasswordResetCompleteView, MyProfileUser#, sign_out, #editProfileUserViews,
    # UserPasswordResetView#, UserRegistrationView #, ActivationView
# from accounts.forms import UserRegistrationForm
#
# from registration.views import RegistrationView

#, UserLoginView
#BCV
# from django.views.generic.base import TemplateView
# from .views import UserRegistrationView
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView)
    # PasswordResetConfirmView,
    # PasswordResetCompleteView)

urlpatterns = [
    # url(r'^logout/$', sign_out, name='logout'),
    url(r'^login/$', login_user, name='login'),
    url(r'^registration/$', registrationView, name='registration'),
    # url(r'^registration/confirm/([\w\-]+)/([\w\-]+)/$', 'accounts.views.confirm_reg', name='confirm-reg'),
    # url(r'^profile-user/$', profileUserViews, name='profile_user'),
    # url(r'^profile-user/edit/$', editProfileUserViews, name='edit_profile_user'),
    url(r'^profile-user/$', MyProfileUser.as_view(), name='profile_user'),
    # url(r'^profile-user/edit/$', UserProfileUpdateViews.as_view(template_name='edit-profile-user.html'),
    #     name='edit_profile'),

    url(r'^profile-user/(?P<pk>\d+)/edit/$', UserProfileUpdateViews.as_view(), name='edit_profile_user'),

    # url(r'^register/$', RegistrationView.as_view(form_class=UserRegistrationForm),
    #     name='registration_register',),

    # url(r'^activate/complete/$',
    #     TemplateView.as_view(
    #         template_name='registration/activation_complete.html'
    #     ),
    #     name='registration_activation_complete'),

    # The activation key can make use of any character from the
    # URL-safe base64 alphabet, plus the colon as a separator.
    # url(r'^activate/(?P<activation_key>[-:\w]+)/$',
    #     ActivationView.as_view(),
    #     name='registration_activate'),

    # CBV------------------

    # url(r'^register/$',
    #     views.RegistrationView.as_view(),
    #     name='registration_register'),
    # url(r'^registration/complete/$',
    #     TemplateView.as_view(
    #         template_name='registration/registration_complete.html'
    #     ),
    #     name='registration_complete'),
    # url(r'^register/closed/$',
    #     TemplateView.as_view(
    #         template_name='registration/registration_closed.html'
    #     ),

    url(r'^signin/$', LoginView.as_view(template_name='signin.html'), name='signin'),
    url(r'^sign_out/$', LogoutView.as_view(), name='sign_out'),
    # url(r'^signout/$', LogoutView.as_view(template_name='main.html'), name='sign_out'),

    url(r'^signup/$', signup, name='signup'),
    url('signup/', SignUp.as_view(), name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),


    url(r'^change-password/$', PasswordChangeView.as_view(template_name='password_change_form.html'),
        name='password_change'),
    url(r'^change-password/done/$', PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),


    url(r'^password_reset/$', PasswordResetView.as_view(template_name='password_reset_form.html'),
        name='password_reset'),
    url(r'^password_reset/done/$', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
    #     name='password_reset_confirm'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        MyUserPasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^password_reset/complete/$', UserPasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    # url(r'^password_reset/complete/$', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
    #     name='password_reset_complete'),

    # url(r'^profile-user/<int:pk>/edit/$', UserProfileUpdateViews.as_view(), name='edit_profile_user'), # for django 2
    # url(r'^forgot-password/$', ForgotPassword, name='ForgotPassword'),
    # url(r'^api/login/$', UserLoginView.as_view()),
]
