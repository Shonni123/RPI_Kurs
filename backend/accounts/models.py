import random
import string
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_email_verified = models.BooleanField(default=False, verbose_name='Email подтвержден')
    phone = models.CharField(max_length=30, blank=True, verbose_name='Телефон')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'{self.user.email or self.user.username} ({"Подтвержден" if self.is_email_verified else "Не подтвержден"})'


class EmailVerificationCode(models.Model):
    class Purpose(models.TextChoices):
        VERIFY_EMAIL = 'verify_email', 'Подтверждение почты'
        RESET_PASSWORD = 'reset_password', 'Сброс пароля'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_codes')
    code = models.CharField(max_length=6, verbose_name='6-значный код')
    purpose = models.CharField(
        max_length=20,
        choices=Purpose.choices,
        default=Purpose.VERIFY_EMAIL,
        verbose_name='Назначение кода'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    is_used = models.BooleanField(default=False, verbose_name='Использован')

    class Meta:
        verbose_name = 'Код подтверждения'
        verbose_name_plural = 'Коды подтверждения'
        ordering = ['-created_at']

    @classmethod
    def generate_for_user(cls, user, purpose=Purpose.VERIFY_EMAIL):
        """
        Удаляет неиспользованные коды пользователя для этой цели и создает новый 6-значный код.
        """
        cls.objects.filter(user=user, purpose=purpose, is_used=False).delete()
        code = ''.join(random.choices(string.digits, k=6))
        return cls.objects.create(user=user, code=code, purpose=purpose)

    def is_expired(self, expiry_minutes=15):
        """
        Проверяет, не истёк ли срок действия кода (по умолчанию 15 минут).
        """
        return timezone.now() > self.created_at + timedelta(minutes=expiry_minutes)

    def __str__(self):
        return f'{self.user.email} - {self.code} ({self.get_purpose_display()})'
