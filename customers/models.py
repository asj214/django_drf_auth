import jwt
from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from configs.models import BaseModel


class CustomerManager(BaseUserManager):

    def __init__(self, *args, **kwargs):
        super(CustomerManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def create_user(self, email, name, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        customer = self.model(email=self.normalize_email(email), name=name, **kwargs)
        customer.set_password(password)
        customer.save(using=self._db)
        return customer


class Customer(AbstractBaseUser, BaseModel):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, default=None, blank=True)

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    class Meta:
        db_table = 'customers'
        ordering = ['-id']

    def __str__(self):
        return self.name

    def delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=settings.JWT_EXPIRE_DAY)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token
