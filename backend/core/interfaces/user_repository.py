"""
Core Layer - User Repository Interface
"""
from abc import abstractmethod
from typing import Optional, List
from core.interfaces.base_repository import BaseRepository
from core.entities.user_entity import UserEntity, UserRole


class IUserRepository(BaseRepository[UserEntity]):
    """Interface untuk User Repository."""

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def get_by_role(self, role: UserRole) -> List[UserEntity]:
        pass

    @abstractmethod
    def count_all(self) -> int:
        pass

    @abstractmethod
    def count_by_role(self, role: UserRole) -> int:
        pass
