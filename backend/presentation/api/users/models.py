"""
Presentation Layer - User Django Model
Model ini adalah implementasi database dari domain entity.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model dengan field role (admin/pelanggan).
    Extend dari AbstractUser untuk dapat fitur auth Django bawaan.
    """

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        PELANGGAN = 'pelanggan', 'Pelanggan'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PELANGGAN,
        verbose_name='Role'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    @property
    def is_pelanggan_role(self):
        return self.role == self.Role.PELANGGAN
