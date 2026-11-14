from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile, EmailVerificationCode


class UserSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source='first_name', read_only=True)
    isEmailVerified = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'fullName',
            'isEmailVerified',
            'phone',
            'date_joined',
        ]

    def get_isEmailVerified(self, obj):
        profile = getattr(obj, 'profile', None)
        return bool(profile and profile.is_email_verified)

    def get_phone(self, obj):
        profile = getattr(obj, 'profile', None)
        return profile.phone if profile else ''


class RegisterSerializer(serializers.Serializer):
    fullName = serializers.CharField(max_length=150, required=False, allow_blank=True)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)
    passwordConfirm = serializers.CharField(min_length=6, write_only=True)

    def validate_email(self, value):
        norm_email = value.lower().strip()
        # Если пользователь с таким email уже существует и подтверждён
        existing = User.objects.filter(email__iexact=norm_email).first()
        if existing:
            profile = getattr(existing, 'profile', None)
            if profile and profile.is_email_verified:
                raise serializers.ValidationError('Пользователь с таким email уже зарегистрирован.')
        return norm_email

    def validate(self, attrs):
        if attrs['password'] != attrs['passwordConfirm']:
            raise serializers.ValidationError({'passwordConfirm': 'Пароли не совпадают.'})
        return attrs


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6, min_length=6)
    purpose = serializers.ChoiceField(
        choices=EmailVerificationCode.Purpose.choices,
        default=EmailVerificationCode.Purpose.VERIFY_EMAIL,
        required=False
    )


class ResendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    purpose = serializers.ChoiceField(
        choices=EmailVerificationCode.Purpose.choices,
        default=EmailVerificationCode.Purpose.VERIFY_EMAIL,
        required=False
    )


class LoginSerializer(serializers.Serializer):
    emailOrUsername = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        login_input = attrs.get('emailOrUsername', '').strip()
        password = attrs.get('password')

        # Пытаемся найти пользователя по email или username
        user = None
        if '@' in login_input:
            user = User.objects.filter(email__iexact=login_input).first()
        if not user:
            user = User.objects.filter(username__iexact=login_input).first()

        if not user or not user.check_password(password):
            raise serializers.ValidationError('Неверный email или пароль.')

        attrs['user'] = user
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6, min_length=6)
    newPassword = serializers.CharField(min_length=6, write_only=True)
    newPasswordConfirm = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        if attrs['newPassword'] != attrs['newPasswordConfirm']:
            raise serializers.ValidationError({'newPasswordConfirm': 'Пароли не совпадают.'})
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(write_only=True)
    newPassword = serializers.CharField(min_length=6, write_only=True)

