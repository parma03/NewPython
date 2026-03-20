"""
Core Layer - Product Repository Interface
"""
from abc import abstractmethod
from typing import List
from core.interfaces.base_repository import BaseRepository
from core.entities.product_entity import ProductEntity


class IProductRepository(BaseRepository[ProductEntity]):
    """Interface untuk Product Repository."""

    @abstractmethod
    def get_by_name(self, name: str) -> List[ProductEntity]:
        pass

    @abstractmethod
    def count_all(self) -> int:
        pass

    @abstractmethod
    def search(self, query: str) -> List[ProductEntity]:
        pass
