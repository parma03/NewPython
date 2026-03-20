"""
Infrastructure Layer - Auto Migration
Menjalankan migrasi database otomatis saat aplikasi start.
Mirip seperti EF Core auto-migration.

Fix: makemigrations dijalankan per-app dengan urutan yang benar
agar custom User model selalu dimigrasikan sebelum app lain (admin, dll).
"""
import logging
import sys
import os

logger = logging.getLogger(__name__)


def run_auto_migration():
    """
    Menjalankan Django migrations secara otomatis.

    Urutan penting:
    1. makemigrations users   ← harus duluan (custom AUTH_USER_MODEL)
    2. makemigrations products
    3. migrate                ← apply semua, termasuk admin, auth, dll.
    """
    # Jangan jalankan ulang saat perintah migrate/makemigrations manual
    skip_commands = {'makemigrations', 'migrate', 'shell', 'dbshell',
                     'test', 'collectstatic', 'createsuperuser'}
    current_command = sys.argv[1] if len(sys.argv) > 1 else ''

    if current_command in skip_commands:
        return

    # Gunakan flag env agar tidak double-run di StatReloader
    if os.environ.get('AUTO_MIGRATE_DONE') == '1':
        return
    os.environ['AUTO_MIGRATE_DONE'] = '1'

    try:
        from django.db import connection
        from django.core.management import call_command
        from django.db.utils import OperationalError

        # ── 1. Cek koneksi database ──────────────────────────────────
        try:
            connection.ensure_connection()
        except OperationalError as e:
            logger.warning(f"⚠️  Database connection failed: {e}")
            logger.warning("   Pastikan PostgreSQL berjalan dan .env sudah dikonfigurasi.")
            os.environ.pop('AUTO_MIGRATE_DONE', None)
            return

        logger.info("🔄 Running auto-migration...")

        # ── 2. makemigrations: users DULU (custom AUTH_USER_MODEL) ────
        # Ini penting agar tabel users ada sebelum admin/auth di-migrate
        for app_label in ('users', 'products'):
            try:
                call_command('makemigrations', app_label, '--no-input', verbosity=0)
            except Exception as e:
                # Bisa terjadi jika migration sudah ada — abaikan
                logger.debug(f"makemigrations {app_label}: {e}")

        # ── 3. migrate semua (apply semua pending migrations) ─────────
        try:
            call_command('migrate', '--no-input', '--run-syncdb', verbosity=1)
            logger.info("✅ Auto-migration selesai.")
        except Exception as e:
            logger.error(f"❌ migrate error: {e}")

    except Exception as e:
        logger.error(f"❌ Auto-migration gagal: {e}")
        os.environ.pop('AUTO_MIGRATE_DONE', None)