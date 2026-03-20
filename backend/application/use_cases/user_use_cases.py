"""
Application Layer - User Use Cases
"""
from typing import List, Optional
from core.interfaces.user_repository import IUserRepository
from core.entities.user_entity import UserEntity, UserRole


class ListUsersUseCase:
    def __init__(self, user_repository: IUserRepository):
        self._repo = user_repository

    def execute(self) -> List[UserEntity]:
        return self._repo.get_all()


class GetUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self._repo = user_repository

    def execute(self, user_id: int) -> Optional[UserEntity]:
        user = self._repo.get_by_id(user_id)
        if not user:
            raise ValueError("User tidak ditemukan.")
        return user


class UpdateUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self._repo = user_repository

    def execute(self, user_id: int, **kwargs) -> UserEntity:
        user = self._repo.get_by_id(user_id)
        if not user:
            raise ValueError("User tidak ditemukan.")
        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        return self._repo.update(user)


class DeleteUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self._repo = user_repository

    def execute(self, user_id: int) -> bool:
        user = self._repo.get_by_id(user_id)
        if not user:
            raise ValueError("User tidak ditemukan.")
        return self._repo.delete(user_id)
