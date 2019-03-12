import traceback

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import UserModel
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['name','nickname','school','etsid','email','id']

