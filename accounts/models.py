from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.manager import CustomUserManager
from django.core.validators import EmailValidator
from accounts import validators as v
import datetime as dt
from django.conf import settings

class User(AbstractUser):
    GENDER = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('x', 'Other')
    )
    username = None
    # profile data
    email = models.EmailField(unique=True, validators=[EmailValidator, v.validate_email])
    phone = models.CharField(max_length=10, unique=True, validators=[v.validate_phone])
    first_name = models.CharField(max_length=150, validators=[v.validate_first_name])
    last_name = models.CharField(max_length=150, blank=True, validators=[v.validate_last_name])
    gender = models.CharField(max_length=10, blank=True, choices=GENDER)
    college = models.CharField(max_length=100, blank=True)
    dob = models.DateField(blank=True, null=True)
    profile_pic = models.FileField(upload_to='profile/', null=True, blank=True)
    last_modified = models.DateField(auto_now=True)
    bio = models.TextField(blank=True, null=True)
    # verification detail
    verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=6,blank=True, null=True)
    email_otp_ts = models.DateTimeField(blank=True, null=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    phone_otp = models.CharField(max_length=6,blank=True, null=True)
    phone_otp_ts = models.DateTimeField(blank=True, null=True)
    phone_verified_at = models.DateTimeField(blank=True, null=True)
    # forgot password
    fget_otp = models.CharField(max_length=6,blank=True, null=True)
    fget_token = models.CharField(max_length=100, null=True, blank=True)
    fget_otp_ts = models.DateTimeField(blank=True, null=True)
    last_fget = models.DateTimeField(blank=True, null=True)
    # suspension
    suspended = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'first_name']

    
    class Meta:
        db_table = "Users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.email} : {self.first_name}'
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
    
    def save(self, *args,**kwargs):
        if not self.email.islower():
            self.email = self.email.strip().lower()
        super().save(*args, **kwargs)