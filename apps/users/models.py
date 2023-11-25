import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number=None, username=None, password=None, **extra_fields):
        with transaction.atomic():
            if not (phone_number or username):
                raise ValueError(_('Either Phone number or Username must be set'))

            if phone_number:
                username = str(uuid.uuid4())[:30]
                while self.model.objects.filter(username=username).exists():
                    username = str(uuid.uuid4())[:30]

            user = self.model(phone_number=phone_number, username=username, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', CustomUser.STAFF)
        return self.create_user(username=username, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    STAFF = 'staff'
    CUSTOMER = 'customer'
    PROVIDER = 'provider'
    USER_TYPES = (
        ('provider', _('Provider')),
        ('customer', _('Customer')),
        ('staff', _('Staff User')),
    )
    user_type = models.CharField(
        _('User Type'),
        max_length=10,
        choices=USER_TYPES
    )

    phone_number = PhoneNumberField(
        _('phonenumber'),
        blank=True,
        null=True,
        unique=True,
        help_text=_("phones start with: '+20'/'+966'")
    )
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True
    )
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    first_name = models.CharField(_('First Name'), max_length=30, null=True, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=30, null=True, blank=True)
    date_joined = models.DateTimeField(_('Date Joined'), auto_now_add=True, null=True)
    language = models.CharField(max_length=10, choices=(('en', 'English'), ('ar', 'Arabic')), default='ar')

    USERNAME_FIELD = 'username'
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        """ for setting unique username if not set(staff)"""
        if not self.username:
            self.username = str(uuid.uuid4())[:30]
        super().save(*args, **kwargs)

    def get_full_name(self):
        full_name = ' '.join(part for part in (self.first_name, self.last_name) if part)
        return full_name if full_name else f"New User {self.pk}"

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _('Custom User')
        verbose_name_plural = _('Custom Users')


class Customer(CustomUser):
    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def save(self, *args, **kwargs):
        self.user_type = CustomUser.CUSTOMER
        super().save(*args, **kwargs)


class Provider(CustomUser):
    class Meta:
        verbose_name = _('Provider')
        verbose_name_plural = _('Providers')

    def save(self, *args, **kwargs):
        self.user_type = CustomUser.PROVIDER
        super().save(*args, **kwargs)


class StaffUser(CustomUser):
    class Meta:
        verbose_name = _('Staff User')
        verbose_name_plural = _('Staff Users')

    def save(self, *args, **kwargs):
        self.user_type = CustomUser.STAFF
        super().save(*args, **kwargs)
