from django.contrib.auth import authenticate
from rest_framework import serializers

from accounts.models import MyCustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyCustomUser
        fields = ('first_name', 'last_name', 'email')
        # fields = ('first_name', 'last_name', 'email', 'password')


class LoginSerialiser(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, max_length=8)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            msg = 'Password or email are not correct'
            raise serializers.ValidationError(msg)
        attrs['user'] = user
        return attrs
