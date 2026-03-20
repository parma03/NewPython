"""
Application Layer - Auth Use Cases
Business logic untuk autentikasi.
"""
from typing import Optional
from core.interfaces.user_repository import IUserRepository
from core.entities.user_entity import UserEntity, UserRole


class RegisterUseCase:
    """Use case untuk registrasi user baru."""

    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    def execute(self, username: str, email: str, password: str, role: str = "pelanggan") -> dict:
        # Validasi username sudah dipakai
        existing = self._user_repository.get_by_username(username)
        if existing:
            raise ValueError("Username sudah digunakan.")

        # Validasi email sudah dipakai
        existing_email = self._user_repository.get_by_email(email)
        if existing_email:
            raise ValueError("Email sudah terdaftar.")

        # Validasi role
        try:
            user_role = UserRole(role)
        except ValueError:
            raise ValueError(f"Role tidak valid. Pilihan: {[r.value for r in UserRole]}")

        entity = UserEntity(
            username=username,
            email=email,
            role=user_role,
        )

        return {"entity": entity, "password": password}


class GetUserProfileUseCase:
    """Use case untuk mendapatkan profil user."""

    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    def execute(self, user_id: int) -> Optional[UserEntity]:
        user = self._user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User tidak ditemukan.")
        return user
