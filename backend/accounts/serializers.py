from rest_framework import serializers
from .models import User, MobileToken
from random import randrange


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        def validation_password(expression, message):
            if expression:
                raise serializers.ValidationError(message)

        validation_password(
            expression=data['password1'] != data['password2'],
            message='Password must match',
        )

        validation_password(
            expression=len(data['password1']) < 8,
            message='the password must be at least 8 characters'
        )

        validation_password(
            expression=not any(i.isdigit() for i in data['password1']),
            message='Password must be at at least 1 number character'
        )

        validation_password(
            expression=not any(i.isalpha() for i in data['password1']),
            message='Password must be at at least 1 letter'
        )
        return data

    def create(self, validated_data):
        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        data['password'] = validated_data['password1']
        data['username'] = validated_data['email']
        return self.Meta.model.objects.create_user(**data)

    class Meta:
        model = User
        read_only_fields = ['id', 'verified_mobile']
        fields = (
            'id',
            'email',
            'mobile',
            'first_name',
            'last_name',
            'role',
            'verified_mobile',
            'password1',
            'password2')


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'mobile',
            'first_name',
            'last_name',
            'role',
            'verified_mobile',
        ]


class MobileTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = MobileToken
        fields = (
            'id',
            'user',
            'token',
            'is_expired',
            'created_at',
            'updated_at'
        )
