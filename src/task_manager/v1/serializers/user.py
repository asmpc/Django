from rest_framework import serializers
from account.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=True, allow_blank=False, max_length=64)
    username = serializers.CharField(required=False, allow_blank=True, max_length=64)
    password = serializers.CharField(required=False, allow_blank=True, max_length=128)
    is_staff = serializers.BooleanField(required=False, default=False)




    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `User instance, given the validated data.
        """
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.password = validated_data.get("password", instance.password)
        instance.is_staff = validated_data.get("is_staff", instance.is_staff)
        instance.save()
        return instance