from rest_framework import serializers
from .models import EmployeeInfo
from django.contrib.auth.models import User
from USERS.models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","email"]

class ProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer()

    class Meta:
        model=Profile
        fields="__all__"


class EmployeeInfoSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()

    class Meta:
        model=EmployeeInfo
        fields="__all__"

    def create(self,validated_data):
        obj=EmployeeInfo.objects.create(**validated_data)
        return obj

