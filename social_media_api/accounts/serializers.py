# accounts/serializers.py
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers_count', read_only=True)
    following_count = serializers.IntegerField(source='following_count', read_only=True)
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'bio', 'profile_picture_url',
            'followers_count', 'following_count'
        ]
        read_only_fields = ['id', 'followers_count', 'following_count']

    def get_profile_picture_url(self, obj):
        request = self.context.get('request')
        if obj.profile_picture and hasattr(obj.profile_picture, 'url'):
            url = obj.profile_picture.url
            return request.build_absolute_uri(url) if request else url
        return None


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio', 'token']

    def create(self, validated_data):
        password = validated_data.pop('password')
        # Use create_user to ensure proper password hashing
        user = get_user_model().objects.create_user(password=password, **validated_data)
        # Create token here so tests can find it
        token, _ = Token.objects.get_or_create(user=user)
        user.token = token.key
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs.get('username'),
            password=attrs.get('password')
        )
        if not user:
            raise serializers.ValidationError('Invalid username or password')
        # Ensure token exists
        token, _ = Token.objects.get_or_create(user=user)
        attrs['user'] = user
        attrs['token'] = token.key
        return attrs
