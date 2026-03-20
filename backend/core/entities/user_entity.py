"""
Core Layer - User Entity (Domain Model)
Tidak bergantung pada framework apapun.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    PELANGGAN = "pelanggan"


@dataclass
class UserEntity:
    """
    Domain entity untuk User.
    Pure Python, tidak bergantung pada Django atau ORM manapun.
    """
    username: str
    email: str
    role: UserRole
    id: Optional[int] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    def is_pelanggan(self) -> bool:
        return self.role == UserRole.PELANGGAN

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role.value,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
