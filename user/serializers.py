from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from user.models import Profile
from poem.models import Poem

from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for profile model"""
    poem_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('subscribers', 'bio', 'instagram', 'poem_count', 'total_subscribers', 'total_subscribed')
        read_only_fields = ('subscribers',)

    def get_poem_count(self, obj):
        return Poem.objects.filter(user=obj.user).count()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user model"""
    profile = ProfileSerializer()

    class Meta:
        model = get_user_model()
        fields = ('pen_name', 'first_name', 'last_name', 'profile')

    def update(self, instance, validated_data):
        instance.pen_name = validated_data['pen_name']
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance_profile = instance.profile
        instance_profile.bio = validated_data['profile']['bio']
        instance_profile.instagram = validated_data['profile']['instagram']
        return instance

class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""
    password2 = serializers.CharField(min_length=8, trim_whitespace=False, style={'input_type': 'password'}, write_only=True)
    email2 = serializers.EmailField(trim_whitespace=True, style={'input_type': 'email'}, write_only=True)
    class Meta:
        model = get_user_model()
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8, 'style': {'input_type': 'password'}}}
        fields = ('email', 'email2', 'pen_name', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        email = attrs.get('email')
        email2 = attrs.get('email2')

        if password != password2:
            msg = {'password2': ['Passwords must match.']}
            raise serializers.ValidationError(msg)

        if email != email2:
            msg = {'email2': ['Emails must match.']}
            raise serializers.ValidationError(msg)

        return attrs

    def create(self, validated_data):
        """"Create a new user with encrypted password and return it"""
        del validated_data['password2']
        del validated_data['email2']
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication objects"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')\

        attrs['user'] = user
        return attrs
