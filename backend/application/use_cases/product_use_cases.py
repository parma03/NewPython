"""
Application Layer - Product Use Cases
"""
from decimal import Decimal
from typing import List, Optional
from core.interfaces.product_repository import IProductRepository
from core.entities.product_entity import ProductEntity


class ListProductsUseCase:
    def __init__(self, repo: IProductRepository):
        self._repo = repo

    def execute(self) -> List[ProductEntity]:
        return self._repo.get_all()


class GetProductUseCase:
    def __init__(self, repo: IProductRepository):
        self._repo = repo

    def execute(self, product_id: int) -> Optional[ProductEntity]:
        product = self._repo.get_by_id(product_id)
        if not product:
            raise ValueError("Produk tidak ditemukan.")
        return product


class CreateProductUseCase:
    def __init__(self, repo: IProductRepository):
        self._repo = repo

    def execute(self, name: str, description: str, price: float, stock: int) -> ProductEntity:
        if price < 0:
            raise ValueError("Harga tidak boleh negatif.")
        if stock < 0:
            raise ValueError("Stok tidak boleh negatif.")

        entity = ProductEntity(
            name=name,
            description=description,
            price=Decimal(str(price)),
            stock=stock,
        )
        return self._repo.create(entity)


class UpdateProductUseCase:
    def __init__(self, repo: IProductRepository):
        self._repo = repo

    def execute(self, product_id: int, **kwargs) -> ProductEntity:
        product = self._repo.get_by_id(product_id)
        if not product:
            raise ValueError("Produk tidak ditemukan.")
        for key, value in kwargs.items():
            if hasattr(product, key) and value is not None:
                setattr(product, key, value)
        return self._repo.update(product)


class DeleteProductUseCase:
    def __init__(self, repo: IProductRepository):
        self._repo = repo

    def execute(self, product_id: int) -> bool:
        product = self._repo.get_by_id(product_id)
        if not product:
            raise ValueError("Produk tidak ditemukan.")
        return self._repo.delete(product_id)


class SearchProductUseCase:
    def __init__(self, repo: IProductRepository):
        self._repo = repo

    def execute(self, query: str) -> List[ProductEntity]:
        return self._repo.search(query)
