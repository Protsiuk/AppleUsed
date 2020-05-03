# -*- coding: utf-8 -*-
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse

from django.contrib.auth import (login as auth_login, logout as auth_logout)
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site

from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.template.loader import render_to_string

from django.views.generic import RedirectView, UpdateView, DetailView
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from accounts.forms import MyCustomUserCreationForm
from accounts.models import MyCustomUser
from accounts.tokens import account_activation_token

from django.http import Http404
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token

from accounts.api.serializers import LoginSerialiser
from django.views.decorators.csrf import csrf_exempt


class LoginUserApiView(APIView):

    def post(self, request, ):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if Token.objects.filter(user=serializer.validated_data['user']).exists():
                token = Token.objects.get(user=serializer.validated_data['user'])
            else:
                token = Token.objects.create(user=serializer.validated_data['user'])
            return Response({'success': True,
                             'token': token.key})
        else:
            return Response(serializer.errors)



class LoginUserView(LoginView):

    """
    Provides the ability to login as a user with a email and password
    """
    template_name = 'login.html'

    def get_success_url(self):
        # return reverse('profile_user', kwargs={'pk': self.kwargs['pk']})
        return reverse('profile_user')


class LogoutUserView(LoginRequiredMixin, RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutUserView, self).get(request, *args, **kwargs)

#--------- verification email


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('profile_user'))
    else:
        if request.method == 'POST':
            form = MyCustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Активация акаунта.'
                message = render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse(u'Пожалуйста подтвердите свой email. Инструкции отправлены на email')
        else:
            form = MyCustomUserCreationForm()
        return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyCustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyCustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        return HttpResponse(u'Спасибо, что присоеденились к нам. Теперь можите использовать свои логин и пароль для авторизации')
    else:
        return HttpResponse(u'Ссылка активации недействительна!')


class MyProfileUser(LoginRequiredMixin, DetailView):
    model = MyCustomUser
    template_name = 'profile-user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(request.user)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class UserProfileUpdateViews(LoginRequiredMixin, UpdateView):
    success_url = '/accounts/profile-user/'
    template_name = 'edit-profile-user.html'
    model = MyCustomUser
    """
    Base view for updating an existing object.
    Using this base class requires subclassing to provide a response mixin.
    """
    fields = ['username', 'first_name', 'last_name', 'birth_day', 'email', 'location_user', 'phone_number_user']

    def get_object(self, queryset=None):
        return self.request.user
