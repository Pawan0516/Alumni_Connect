from rest_framework import serializers
from organization.models import College, Address, SocialLink, User
from rest_framework.validators import UniqueValidator
from accounts import validators as v
from django.contrib.auth.password_validation import validate_password

class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ["type", "url"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["city", "state", "country", "postal_code"]


class CollegeSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    socials = SocialLinkSerializer(many=True, read_only=True)

    class Meta:
        model = College
        fields = [
            "id",
            "name",
            "handle",
            "website",
            "established_date",
            "line1",
            "line2",
            "address",
            "socials",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")



class OnboardSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = [
            'email', 'password'
        ]
        extra_kwargs = {
            'email': {
                'validators': [v.validate_email],
                'required': True
            },
            'password': {
                'write_only': True,
                'required': True,
                'validators': [v.validate_password, validate_password]
            },
        }

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user