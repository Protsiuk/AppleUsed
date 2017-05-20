from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from accounts.serializers import LoginSerializer
from accounts.forms import LoginForm


def main_page(request):
    return render(request, "main.html")


@login_required(login_url="/login/")
def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse("main"))


def sign_in(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("main"))
    else:
        form = LoginForm()
        if request.method == "main":
            form = LoginForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user = authenticate(email=data.get("email"), password=data.get("password"))
                if user:
                    login(request, user)
                    return HttpResponseRedirect(reverse("main"))
                else:
                    print("sorry")
        return render(request, "login.html", {"form": form})


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
