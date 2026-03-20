"""
Core Layer - Product Entity (Domain Model)
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal


@dataclass
class ProductEntity:
    """
    Domain entity untuk Product/Barang.
    Pure Python, tidak bergantung pada framework.
    """
    name: str
    description: str
    price: Decimal
    stock: int
    id: Optional[int] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_available(self) -> bool:
        return self.is_active and self.stock > 0

    def reduce_stock(self, quantity: int) -> None:
        if quantity > self.stock:
            raise ValueError(f"Stok tidak mencukupi. Stok tersedia: {self.stock}")
        self.stock -= quantity

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "stock": self.stock,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
