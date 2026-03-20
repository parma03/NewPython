"""
Application Layer - Analytics Service
"""
from core.interfaces.user_repository import IUserRepository
from core.interfaces.product_repository import IProductRepository
from core.entities.user_entity import UserRole


class AnalyticsService:
    """Service untuk mengumpulkan data analytics dashboard."""

    def __init__(self, user_repo: IUserRepository, product_repo: IProductRepository):
        self._user_repo = user_repo
        self._product_repo = product_repo

    def get_dashboard_stats(self) -> dict:
        """Mengambil statistik untuk dashboard admin."""
        return {
            "total_users": self._user_repo.count_all(),
            "total_admin": self._user_repo.count_by_role(UserRole.ADMIN),
            "total_pelanggan": self._user_repo.count_by_role(UserRole.PELANGGAN),
            "total_products": self._product_repo.count_all(),
        }

    def get_user_stats(self) -> dict:
        """Mengambil statistik user saja (untuk pelanggan)."""
        return {
            "total_users": self._user_repo.count_all(),
            "total_admin": self._user_repo.count_by_role(UserRole.ADMIN),
            "total_pelanggan": self._user_repo.count_by_role(UserRole.PELANGGAN),
        }
