"""
Infrastructure Layer - Product Repository Implementation
"""
from typing import Optional, List
from core.interfaces.product_repository import IProductRepository
from core.entities.product_entity import ProductEntity
from decimal import Decimal


class DjangoProductRepository(IProductRepository):
    """Implementasi product repository dengan Django ORM."""

    def _get_model(self):
        from presentation.api.products.models import Product
        return Product

    def _to_entity(self, db_obj) -> ProductEntity:
        return ProductEntity(
            id=db_obj.id,
            name=db_obj.name,
            description=db_obj.description,
            price=db_obj.price,
            stock=db_obj.stock,
            is_active=db_obj.is_active,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at,
        )

    def get_by_id(self, id: int) -> Optional[ProductEntity]:
        Product = self._get_model()
        try:
            return self._to_entity(Product.objects.get(pk=id))
        except Product.DoesNotExist:
            return None

    def get_all(self) -> List[ProductEntity]:
        Product = self._get_model()
        return [self._to_entity(p) for p in Product.objects.all().order_by('-created_at')]

    def get_by_name(self, name: str) -> List[ProductEntity]:
        Product = self._get_model()
        return [self._to_entity(p) for p in Product.objects.filter(name__icontains=name)]

    def count_all(self) -> int:
        Product = self._get_model()
        return Product.objects.count()

    def search(self, query: str) -> List[ProductEntity]:
        Product = self._get_model()
        qs = Product.objects.filter(name__icontains=query) | \
             Product.objects.filter(description__icontains=query)
        return [self._to_entity(p) for p in qs.distinct()]

    def create(self, entity: ProductEntity) -> ProductEntity:
        Product = self._get_model()
        obj = Product.objects.create(
            name=entity.name,
            description=entity.description,
            price=entity.price,
            stock=entity.stock,
            is_active=entity.is_active,
        )
        return self._to_entity(obj)

    def update(self, entity: ProductEntity) -> ProductEntity:
        Product = self._get_model()
        obj = Product.objects.get(pk=entity.id)
        obj.name = entity.name
        obj.description = entity.description
        obj.price = entity.price
        obj.stock = entity.stock
        obj.is_active = entity.is_active
        obj.save()
        return self._to_entity(obj)

    def delete(self, id: int) -> bool:
        Product = self._get_model()
        try:
            Product.objects.get(pk=id).delete()
            return True
        except Product.DoesNotExist:
            return False
