from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from accounts import validators as v
from accounts.models import User, UserDetail


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", 'org_admin', "date_joined")


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ["phone", "first_name", "last_name", "gender", "dob", "bio", "profile_pic"]


class ProfileSerializer(serializers.ModelSerializer):
    user_detail = UserDetailSerializer(allow_null=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "org_admin", "is_suspended", "is_verified", "date_joined", "user_detail")


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ["phone", "first_name", "last_name", "gender", "dob", "bio", "profile_pic"]
        extra_kwargs = {
            "phone": {"validators": [v.validate_phone]},
            "first_name": {"validators": [v.validate_first_name]},
            "last_name": {"default": "", "validators": [v.validate_last_name]},
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[v.validate_password, validate_password])
