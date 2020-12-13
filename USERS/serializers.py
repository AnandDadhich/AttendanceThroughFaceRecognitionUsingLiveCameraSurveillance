from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions

class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['username','password']

    def validate(self,data):
        username=data.get("username")
        password=data.get("password")

        if username and password:
            user=authenticate(username=username,password=password)

            if user:
                if user.is_active:
                    data['user']=user
                else:
                    msg="User is deactivated"
                    return exceptions.ValidationError(msg)
            else:
                msg="Unable to login with given credentials means username and password not match"
                raise exceptions.ValidationError(msg)
        else:
            msg="Must provide Username and Password both."
            raise exceptions.ValidationError(msg)

        return data


