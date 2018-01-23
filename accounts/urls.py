from django.conf.urls import url

from accounts.views import sign_out, sign_in, registrationView, profileUserViews, editProfileUserViews #, UserLoginView

urlpatterns = [
    url(r'^logout/$', sign_out, name='logout'),
    url(r'^login/$', sign_in, name='login'),
    url(r'^registration/$', registrationView, name='registration'),
    url(r'^profile-user/$', profileUserViews, name='profile_user'),

    url(r'^edit-profile-user/$', editProfileUserViews, name='edit_profile_user'),

    # url(r'^change-password/$', ChangePasswordViews, name='Change_password'),
    # url(r'^change-password-done/$', ChangePasswordDoneViews, name='Change_password'),

    # url(r'^password_reset/$',PasswordResetView, name='password_reset'),
    # url(r'^password_reset/done/$', PasswordResetDoneView, name='password_reset_done'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     PasswordResetConfirmView,name='password_reset_confirm'),
    # url(r'^reset/done/$', PasswordResetCompleteView, name='password_reset_complete'),

    # url(r'^forgot-password/$', ForgotPassword, name='ForgotPassword'),
    # url(r'^api/login/$', UserLoginView.as_view()),
]
