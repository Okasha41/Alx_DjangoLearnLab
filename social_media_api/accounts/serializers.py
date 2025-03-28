from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import CustomeUserModel


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     style={'input_type': 'password'})
    confirm_password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'})
    token = serializers.SerializerMethodField()

    class Meta:
        model = CustomeUserModel
        fields = ['id', 'username', 'password', 'email',
                  'confirm_password', 'bio', 'profile_picture', 'token']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {'confirm_password': 'Passwords do not match'}
            )
        return data

    def create(self, validated_data):
        # Remove confirm_password
        validated_data.pop('confirm_password', None)

        # Ensure only valid fields are passed
        user_data = {
            'username': validated_data.get('username'),
            'email': validated_data.get('email'),
            'password': validated_data.get('password'),
        }

        # Optional bio
        if 'bio' in validated_data:
            user_data['bio'] = validated_data['bio']

        user = CustomeUserModel.objects.create_user(**validated_data)
        # get_user_model().objects.create_user(**validated_data)
        return user

    def get_token(self, obj):
        token = Token.objects.create(user=obj)
        return token.key


class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            username=username,
            password=password,
            request=self.context.get('request')
        )

        if not user:
            return serializers.ValidationError('Could not login with the provided credentials')

        attrs['user'] = user

        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomeUserModel
        fields = ['id', 'username', 'email', 'bio',
                  'profile_picture', 'followers_count', 'following_count']
        read_only_fields = ['id', 'username',
                            'followers_count', 'following_count']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()
