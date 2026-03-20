"""
Users App Configuration
Auto-migration dijalankan dari sini saat app ready.
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'presentation.api.users'
    label = 'users'
    verbose_name = 'Users'

    def ready(self):
        """
        Dipanggil saat Django app sudah siap.
        Jalankan auto-migration seperti EF Core pada startup.
        """
        from infrastructure.database.auto_migrate import run_auto_migration
        run_auto_migration()
