"""
Presentation Layer - Product Django Model
"""
from django.db import models


class Product(models.Model):
    """Model untuk data barang/produk."""

    name = models.CharField(max_length=255, verbose_name='Nama Barang')
    description = models.TextField(blank=True, verbose_name='Deskripsi')
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Harga')
    stock = models.IntegerField(default=0, verbose_name='Stok')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} (Stok: {self.stock})"
