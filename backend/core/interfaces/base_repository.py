"""
Core Layer - Base Repository Interface
Defines the contract that all repositories must implement.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """Abstract base repository - kontrak untuk semua repository."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def create(self, entity: T) -> T:
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
