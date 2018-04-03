from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from rest_framework import serializers

from rest_framework.serializers import (
    CharField,EmailField,HyperlinkedIdentityField,ModelSerializer,SerializerMethodField,ValidationError
    )
from .models import *
User = get_user_model()

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username','email','first_name','last_name',
        ]

class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email Address')
    email2 = EmailField(label='Confirm Email')
    class Meta:
        model = User
        fields = [
            'username','email','email2','password',
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                            }
    def validate(self, data):
        email = data['email']
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")
        return data

    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email2")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")

        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")

        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise ValidationError({'status': 401,'message': 'Make sure both email must match','error':"Emails must match.",'username':data.get("username")})
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
                username = username,
                email = email
            )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data



class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField()
    email = EmailField(label='Email Address')
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                            }
    def validate(self, data):
        email = data['email']
        username = data['username']
        password = data['password']
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return data
            else:
                return ValidationError({'status': 400,'message': 'Make sure your email and password are correct','error':"Password does not match",'username': username })
        except User.DoesNotExist:
            raise ValidationError({'status': 400,'message': 'Make sure your email and password are correct','error':"User does not exist",'username': username })

class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')

class ProfileCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['gender','address','nationality']

    def create(self, validated_data):
        user = validated_data['user']
        gender = validated_data['gender']
        address = validated_data['address']
        prof_obj = Profile(
                gender = gender,
                address = address
            )
        prof_obj.user = user
        prof_obj.save()
        return validated_data

    def update(self, instance, validated_data):
        instance.gender = validated_data.get('gender', instance.gender)
        instance.address = validated_data.get('address', instance.address)
        instance.nationality = validated_data.get('nationality', instance.nationality)
        instance.save()
        return instance
