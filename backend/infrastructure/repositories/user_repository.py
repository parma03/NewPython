"""
Infrastructure Layer - User Repository Implementation
Mengimplementasikan IUserRepository menggunakan Django ORM.
"""
from typing import Optional, List
from core.interfaces.user_repository import IUserRepository
from core.entities.user_entity import UserEntity, UserRole


class DjangoUserRepository(IUserRepository):
    """Implementasi user repository dengan Django ORM."""

    def _get_model(self):
        from django.contrib.auth import get_user_model
        return get_user_model()

    def _to_entity(self, db_obj) -> UserEntity:
        return UserEntity(
            id=db_obj.id,
            username=db_obj.username,
            email=db_obj.email,
            role=UserRole(db_obj.role),
            is_active=db_obj.is_active,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at,
        )

    def get_by_id(self, id: int) -> Optional[UserEntity]:
        User = self._get_model()
        try:
            obj = User.objects.get(pk=id)
            return self._to_entity(obj)
        except User.DoesNotExist:
            return None

    def get_all(self) -> List[UserEntity]:
        User = self._get_model()
        return [self._to_entity(u) for u in User.objects.all().order_by('-created_at')]

    def get_by_username(self, username: str) -> Optional[UserEntity]:
        User = self._get_model()
        try:
            return self._to_entity(User.objects.get(username=username))
        except User.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> Optional[UserEntity]:
        User = self._get_model()
        try:
            return self._to_entity(User.objects.get(email=email))
        except User.DoesNotExist:
            return None

    def get_by_role(self, role: UserRole) -> List[UserEntity]:
        User = self._get_model()
        return [self._to_entity(u) for u in User.objects.filter(role=role.value)]

    def count_all(self) -> int:
        User = self._get_model()
        return User.objects.count()

    def count_by_role(self, role: UserRole) -> int:
        User = self._get_model()
        return User.objects.filter(role=role.value).count()

    def create(self, entity: UserEntity, password: str = None) -> UserEntity:
        User = self._get_model()
        obj = User(
            username=entity.username,
            email=entity.email,
            role=entity.role.value,
            is_active=entity.is_active,
        )
        if password:
            obj.set_password(password)
        obj.save()
        return self._to_entity(obj)

    def update(self, entity: UserEntity) -> UserEntity:
        User = self._get_model()
        obj = User.objects.get(pk=entity.id)
        obj.username = entity.username
        obj.email = entity.email
        obj.role = entity.role.value
        obj.is_active = entity.is_active
        obj.save()
        return self._to_entity(obj)

    def delete(self, id: int) -> bool:
        User = self._get_model()
        try:
            User.objects.get(pk=id).delete()
            return True
        except User.DoesNotExist:
            return False
