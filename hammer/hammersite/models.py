import random
import string
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import timedelta

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, **extra_fields):
        if not phone_number:
            raise ValueError('Номер телефона обязателен')
        # Генерация случайного инвайт-кода (6 символов: цифры и буквы)
        invite_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        # Создание пользователя с инвайт-кодом
        user = self.model(phone_number=phone_number, invite_code=invite_code, **extra_fields)
        user.set_password(extra_fields.get('password', None))  # Для возможного пароля
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    invite_code = models.CharField(max_length=6)
    activate_invite_code = models.BooleanField(default=False)
    code = models.CharField(max_length=4, blank=True, null=True)
    code_expires_at = models.DateTimeField(null=True, blank=True)  # Время истечения кода
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    invited_users = models.ManyToManyField('self', symmetrical=False, related_name='invited_by')

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

    def set_code(self, code):
        """Устанавливает код подтверждения и время истечения."""
        self.code = code
        self.code_expires_at = timezone.now() + timedelta(minutes=5)  # Код действует 5 минут
        self.save()

    def verify_code(self, code):
        """Проверяет код и его срок действия."""
        if self.code == code and self.code_expires_at > timezone.now():
            return True
        return False
