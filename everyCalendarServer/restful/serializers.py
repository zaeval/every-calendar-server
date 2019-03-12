import traceback

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import UserModel
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework import mixins

class FriendSerializer(serializers.Serializer):
    name=serializers.CharField()
    userid=serializers.CharField()