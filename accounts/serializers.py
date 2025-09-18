from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts import validators as v
from accounts.models import User

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name','gender', 'college', 'phone', 'email', 'date_joined'
        )

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'gender', 'college', 'phone', 'email','suspended','verified', 'date_joined'
        )

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'gender', 'college', 'phone'
        )
        extra_kwargs = {
            'phone': {
                'validators': [v.validate_phone],
                'required': True
            },
            'first_name': {'required': True, 'validators': [v.validate_first_name]},
            'last_name': {'default':'', 'validators': [v.validate_last_name]},
            'gender': {'required': True, 'validators': [v.validate_gender]},
            'college': {'required': True, 'validators': [v.validate_college]},
        }

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class RegisterSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = [
            'email', 'phone', 'first_name', 'last_name',
            'gender', 'college', 'password'
        ]
        extra_kwargs = {
            'email': {
                'validators': [v.validate_email],
                'required': True
            },
            'phone': {
                'validators': [v.validate_phone],
                'required': True
            },
            'first_name': {'required': True, 'validators': [v.validate_first_name]},
            'last_name': {'default':'', 'validators': [v.validate_last_name]},
            'gender': {'required': True, 'validators': [v.validate_gender]},
            'college': {'required': True, 'validators': [v.validate_college]},
            'password': {
                'write_only': True,
                'required': True,
                'validators': [v.validate_password, validate_password]
            },
        }

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            phone=validated_data['phone'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            gender=validated_data['gender'],
            college=validated_data['college'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user