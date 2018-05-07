from django.conf.urls import url#, include

from accounts.views import sign_out, sign_in, registrationView, profileUserViews, editProfileUserViews#, UserRegistrationView #, ActivationView
# from accounts.forms import UserRegistrationForm

# from registration.views import RegistrationView

#, UserLoginView
# from django.views.generic.base import TemplateView
# from .views import UserRegistrationView


urlpatterns = [
    url(r'^logout/$', sign_out, name='logout'),
    url(r'^login/$', sign_in, name='login'),
    url(r'^registration/$', registrationView, name='registration'),
    # url(r'^registration/confirm/([\w\-]+)/([\w\-]+)/$', 'accounts.views.confirm_reg', name='confirm-reg'),
    url(r'^profile-user/$', profileUserViews, name='profile_user'),
    url(r'^profile-user/edit/$', editProfileUserViews, name='edit_profile_user'),

    # url(r'^register/$', RegistrationView.as_view(form_class=UserRegistrationForm),
    #     name='registration_register',),

    # url(r'^', include('registration.backends.default.urls')),

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
]

    # url(r"^verify-email/$", email_verification_sent, name="account_email_verification_sent"),


    # url(r'^verify-email/$', VerifyEmailView.as_view(), name='rest_verify_email'),
    # url(r'^email-verification/$', TemplateView.as_view(template_name="email_verification.html"), name='email-verification'),

    # url(r'^change-password/$', ChangePasswordViews, name='Change_password'),
    # url(r'^change-password-done/$', ChangePasswordDon   # url(r'^password_reset/$',PasswordResetView, name='password_reset'),
    # url(r'^password_reset/done/$', PasswordResetDoneView, name='password_reset_done'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     PasswordResetConfirmView,name='password_reset_confirm'),
    # url(r'^reset/done/$', PasswordResetCompleteView, name='password_reset_complete'),

    # url(r'^forgot-password/$', ForgotPassword, name='ForgotPassword'),
    # url(r'^api/login/$', UserLoginView.as_view()),

