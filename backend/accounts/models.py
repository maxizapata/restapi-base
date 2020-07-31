from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from random import randrange


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class User(AbstractUser):
    # Rider and Driver roles
    ROLE_CHOICES = (
        (1, 'driver'),
        (2, 'rider'),
        (3, 'admin')
    )

    email = models.EmailField(unique=True, blank=False, null=False)
    mobile = PhoneNumberField(blank=False, null=False)
    verified_mobile = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='profile_pics')
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES,
        null=False,
        blank=False
    )

    # Login and signup settings
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'role', 'mobile',)

    def __str__(self):
        return self.email

    def get_mobile(self, plus=False):
        return f'+{str(self.mobile.country_code)}{str(self.mobile.national_number)}'

    def get_token_header(self, auth=False):
        return f'Token {self.auth_token.key}'


class MobileToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING
    )
    token = models.CharField(max_length=6)
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.token
