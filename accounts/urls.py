from django.conf.urls import url

from accounts.views import (
    UserProfileUpdateViews,
    LoginUserView,
    LogoutUserView,
    signup,
    activate,
    MyProfileUser)

from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView)

urlpatterns = [

    # -------------CBV------------------

    url(r'^signup/$', signup, name='signup'), #it's worked

    url(r'^login/$', LoginUserView.as_view(), name='login'),
    url(r'^logout/$', LogoutUserView.as_view(), name='logout'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),

    url(r'^profile-user/$', MyProfileUser.as_view(), name='profile_user'),
    url(r'^profile-user/(?P<pk>\d+)/edit/$', UserProfileUpdateViews.as_view(), name='edit_profile_user'),

    url(r'^change-password/$', PasswordChangeView.as_view(template_name='password_change_form.html'),
        name='password_change'),
    url(r'^change-password/done/$', PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),

    url(r'^password_reset/$', PasswordResetView.as_view(template_name='password_reset_form.html'),
        name='password_reset'),
    url(r'^password_reset/done/$', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'^password_reset/complete/$',
        PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
]
