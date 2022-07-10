from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password

# Create your models here.

class User(AbstractBaseUser):
    email = models.EmailField(unique = True, max_length = 255)
    nickname = models.CharField(max_length = 255, unique = True)
    name = models.CharField(max_length = 255, blank = True, null = True)
    surname = models.CharField(max_length = 255, blank = True, null = True)
    is_staff = models.BooleanField(default = False)
    is_admin = models.BooleanField(dafault = False)
    created_at = models.DateTimeField(auto_now_add = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = BaseUserManager()

    def _create_user(self, email, password = None, nickname = None, name = None, surname = None, is_staff = None, is_admin = None):
        if not email:
            raise ValueError('Введите email')
        if not password:
            raise ValueError('Введите пароль')
        if not nickname:
            raise ValueError('Введите nickname')
        user = self.model(email = email, name = nickname)
        user.is_staff = is_staff
        user.is_admin = is_admin
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password = None, nickname = None, name = None, surname = None, is_staff = None, is_admin = None):
        user = self._create_user(email, password, nickname, name, surname, is_staff=True, is_admin=True)
        return user

    def create_staffuser(self, email, password = None, nickname = None, name = None, surname = None, is_staff = None, is_admin = None):
        user = self._create_user(email, password, nickname, name, surname, is_staff=True, is_admin=False)
        return user

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        else
            return self.is_staff

    @property
    def is_admin(self):
        return self.is_admin

    def save(self, *args, **kwargs):
        if not self.id and not self.is_staff and not self.is_admin:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)