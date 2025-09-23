from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.manager import CustomUserManager
from django.core.validators import EmailValidator
from accounts import validators as v
import datetime as dt


class UserDetail(models.Model):
    GENDER = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('x', 'Other')
    )
    # profile data
    phone = models.CharField(max_length=10, unique=True, validators=[v.validate_phone])
    first_name = models.CharField(max_length=150, validators=[v.validate_first_name])
    last_name = models.CharField(max_length=150, blank=True, validators=[v.validate_last_name])
    gender = models.CharField(max_length=10, blank=True, choices=GENDER)
    dob = models.DateField(blank=True, null=True)
    profile_pic = models.FileField(upload_to='profile/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_details"
        verbose_name = "User Detail"
        verbose_name_plural = "User Details"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.phone} - {self.first_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, validators=[EmailValidator, v.validate_email])
    last_modified = models.DateField(auto_now=True)

    user_detail = models.OneToOneField(UserDetail, null=True, blank=True, on_delete=models.SET_NULL, related_name="user")
    org_admin = models.BooleanField(default=False)
    
    # verification detail
    is_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=6,blank=True, null=True)
    email_otp_ts = models.DateTimeField(blank=True, null=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    
    # forgot password
    foget_otp = models.CharField(max_length=6,blank=True, null=True)
    foget_token = models.CharField(max_length=100, null=True, blank=True)
    foget_otp_ts = models.DateTimeField(blank=True, null=True)
    last_forgeted_at = models.DateTimeField(blank=True, null=True)
    
    # suspension
    is_suspended = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = "auth_account"
        verbose_name = "Auth Account"
        verbose_name_plural = "Auth Accounts"
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.email}'
    
    def save(self, *args,**kwargs):
        if not self.email.islower():
            self.email = self.email.strip().lower()
        super().save(*args, **kwargs)
