# Create your models here.
"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.save(using=self._db)

        # # Create a Technician record for non-staff users
        if user.is_staff:
            Technician.objects.create(user=user)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = False
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Branch(models.Model):
    """Branch object."""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Technician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.ManyToManyField('Skill')
    branches = models.ManyToManyField('Branch')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    format_code = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description


class Discount(models.Model):
    description = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description


class Promo(models.Model):
    WEEKDAYS = [
        (1, 'Lunes'),
        (2, 'Martes'),
        (3, 'Miércoles'),
        (4, 'Jueves'),
        (5, 'Viernes'),
        (6, 'Sábado'),
        (7, 'Domingo'),
    ]
    weekday = models.IntegerField(choices=WEEKDAYS)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    birthday = models.DateField()
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} {self.last_name}'


class Appointment(models.Model):

    #TODO - Add created_by field
    date = models.DateField()
    time = models.TimeField()
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    technician = models.ForeignKey('Technician', on_delete=models.CASCADE)
    warranty = models.BooleanField(default=False)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE,
                                null=True, blank=True)
    commission = models.DecimalField(max_digits=10, decimal_places=2,
                                     default=0.00)
    tip = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    courtesy = models.DecimalField(max_digits=10, decimal_places=2,
                                   default=0.00)
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE,
                                 null=True, blank=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2,
                                         default=0.00)
    final_income = models.DecimalField(max_digits=10, decimal_places=2,
                                       default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.date} - {self.time} - {self.client}'
