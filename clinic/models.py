from django.db import models
from django.contrib.auth.models import User, Group


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_profile',
        null=True
    )
    role = models.CharField(max_length=30, null=True)
    password = models.CharField(max_length=150, null=True)
    mobile = models.CharField(max_length=20, null=True)
    national_code = models.CharField(max_length=15, null=True)
    province = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)


class Reception(models.Model):
    doctor = models.ForeignKey(
        UserProfile,
        related_name='doctor',
        on_delete=models.CASCADE,
        null=True
    )
    title = models.CharField(max_length=50, null=True)
    time = models.DateTimeField(auto_now=True, null=True)
    in_use = models.BooleanField(default=False, null=True)

    def save(self, *args, **kwargs):
        super(Reception, self).save(*args, **kwargs)


class ReserveReception(models.Model):
    reception = models.ForeignKey(
        Reception,
        on_delete=models.CASCADE,
        related_name='reception',
        null=True
    )
    patient = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='patient',
        null=True
    )
    is_available = models.BooleanField(default=True, null=True)

    def save(self, *args, **kwargs):
        super(ReserveReception, self).save(*args, **kwargs)


class Visit(models.Model):
    reception = models.OneToOneField(
        Reception,
        on_delete=models.CASCADE,
        null=True
    )
    result = models.TextField(null=True)

    def save(self, *args, **kwargs):
        super(Visit, self).save(*args, **kwargs)
