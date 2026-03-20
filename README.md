# AppSystem — Django + AngularJS + PostgreSQL

Aplikasi manajemen dengan **Clean Architecture**, **role-based access (Admin & Pelanggan)**, dan **auto-migration** database layaknya Entity Framework Core.

---

## 📁 Struktur Project (Clean Architecture)

```
project/
├── backend/                        ← Django (REST API)
│   ├── core/                       ← 🟣 DOMAIN LAYER (Pure Python)
│   │   ├── entities/
│   │   │   ├── user_entity.py      ← Domain entity User
│   │   │   └── product_entity.py   ← Domain entity Product
│   │   └── interfaces/
│   │       ├── base_repository.py  ← Abstract base repository
│   │       ├── user_repository.py  ← Interface IUserRepository
│   │       └── product_repository.py
│   │
│   ├── application/                ← 🔵 APPLICATION LAYER (Use Cases)
│   │   ├── use_cases/
│   │   │   ├── auth_use_cases.py   ← Register, Get Profile
│   │   │   ├── user_use_cases.py   ← CRUD User
│   │   │   └── product_use_cases.py← CRUD Product
│   │   └── services/
│   │       └── analytics_service.py← Dashboard statistics
│   │
│   ├── infrastructure/             ← 🟠 INFRASTRUCTURE LAYER (DB)
│   │   ├── database/
│   │   │   └── auto_migrate.py     ← ✨ Auto-migration on startup
│   │   └── repositories/
│   │       ├── user_repository.py  ← Django ORM implementation
│   │       └── product_repository.py
│   │
│   ├── presentation/               ← 🟢 PRESENTATION LAYER (API)
│   │   └── api/
│   │       ├── auth/               ← Login, Register, Logout, Profile
│   │       ├── users/              ← CRUD User (Admin only)
│   │       │   ├── models.py       ← Django Model (Custom User)
│   │       │   └── apps.py         ← AppConfig trigger auto-migrate
│   │       └── products/           ← CRUD Product
│   │           └── models.py       ← Django Model (Product)
│   │
│   ├── config/                     ← Django settings, urls, wsgi
│   ├── requirements.txt
│   └── manage.py
│
├── frontend/                       ← AngularJS (SPA)
│   ├── index.html                  ← Entry point
│   └── app/
│       ├── app.js                  ← Root module + Router config
│       ├── modules/
│       │   ├── auth/               ← Login & Register
│       │   ├── dashboard/          ← Analytics dashboard
│       │   ├── products/           ← Kelola barang (Admin)
│       │   └── users/              ← Kelola user (Admin)
│       ├── shared/
│       │   ├── interceptors/
│       │   │   └── auth.interceptor.js ← Auto-attach JWT token
│       │   └── components/
│       │       └── sidebar/        ← Sidebar navigation
│       └── assets/css/styles.css   ← Semua styling
│
├── docker-compose.yml
└── setup.sh
```

---

## 🗺️ Installation Roadmap

### Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.9+ | [python.org](https://python.org) |
| PostgreSQL | 15+ | [postgresql.org](https://postgresql.org) |
| pip | latest | bawaan Python |

---

### Option A: Setup Manual (Tanpa Docker)

#### Step 1 — Clone / Download project

```bash
cd project/
```

#### Step 2 — Buat Database PostgreSQL

```bash
# Masuk ke PostgreSQL
psql -U postgres

# Di dalam psql:
CREATE DATABASE appdb;
\q
```

#### Step 3 — Setup Backend

```bash
cd backend

# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy file .env
cp .env.example .env
```

#### Step 4 — Konfigurasi `.env`

Edit file `backend/.env`:
```env
SECRET_KEY=your-secret-key-ganti-ini
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=appdb
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

#### Step 5 — Jalankan Backend

```bash
# Dari folder backend/ dengan venv aktif:
python manage.py runserver
```

> **✨ Auto-Migration:** Saat `runserver` pertama kali dijalankan:
> 1. Django mendeteksi database kosong
> 2. `AppConfig.ready()` memanggil `run_auto_migration()`
> 3. `makemigrations` + `migrate` berjalan otomatis
> 4. Semua tabel terbuat → siap digunakan!

Output yang diharapkan:
```
🔄 Checking database migrations...
✅ makemigrations completed
Operations to perform: Apply all migrations...
✅ Auto-migration completed successfully
Starting development server at http://127.0.0.1:8000/
```

#### Step 6 — Buat Admin User (Opsional)

```bash
# Masih di folder backend/ dengan venv aktif:
python manage.py createsuperuser
```

Atau langsung daftar via endpoint API / halaman register.

#### Step 7 — Jalankan Frontend

```bash
cd ../frontend

# Gunakan Python simple HTTP server:
python3 -m http.server 5500
```

Buka browser: **http://localhost:5500**

---

### Option B: Setup dengan Docker

```bash
# Dari root project/:
docker-compose up -d
```

Akses:
- Frontend: **http://localhost:5500** (serve manual)
- Backend API: **http://localhost:8000**
- Database: `localhost:5432`

---

## 🔌 API Endpoints

### Authentication
| Method | URL | Auth | Deskripsi |
|--------|-----|------|-----------|
| POST | `/api/v1/auth/register/` | ❌ | Registrasi user baru |
| POST | `/api/v1/auth/login/` | ❌ | Login → dapat JWT token |
| POST | `/api/v1/auth/logout/` | ✅ | Logout + blacklist token |
| GET | `/api/v1/auth/profile/` | ✅ | Data profil user login |
| GET | `/api/v1/auth/dashboard-stats/` | ✅ | Statistik dashboard |
| POST | `/api/v1/auth/token/refresh/` | ❌ | Refresh JWT token |

### Users (Admin Only)
| Method | URL | Deskripsi |
|--------|-----|-----------|
| GET | `/api/v1/users/` | List semua user |
| POST | `/api/v1/users/` | Tambah user baru |
| GET | `/api/v1/users/{id}/` | Detail user |
| PUT | `/api/v1/users/{id}/` | Update user |
| DELETE | `/api/v1/users/{id}/` | Hapus user |

### Products
| Method | URL | Auth | Deskripsi |
|--------|-----|------|-----------|
| GET | `/api/v1/products/` | ✅ All | List semua produk |
| POST | `/api/v1/products/` | ✅ Admin | Tambah produk |
| GET | `/api/v1/products/{id}/` | ✅ All | Detail produk |
| PUT | `/api/v1/products/{id}/` | ✅ Admin | Update produk |
| DELETE | `/api/v1/products/{id}/` | ✅ Admin | Hapus produk |

---

## 👤 Role & Permissions

| Fitur | Admin | Pelanggan |
|-------|-------|-----------|
| Dashboard Analytics (User Stats) | ✅ | ✅ |
| Dashboard Analytics (Product Stats) | ✅ | ❌ |
| Kelola Barang (CRUD) | ✅ | ❌ |
| Kelola User (CRUD) | ✅ | ❌ |
| Lihat Daftar Produk | ✅ | ✅ |

---

## 🏛️ Clean Architecture Layers

```
┌─────────────────────────────────────────┐
│         PRESENTATION LAYER              │  ← API Views, Serializers, Django Models
│         (Django REST Framework)         │
├─────────────────────────────────────────┤
│         APPLICATION LAYER              │  ← Use Cases, Services (Business Logic)
│         (Pure Python)                  │
├─────────────────────────────────────────┤
│         INFRASTRUCTURE LAYER           │  ← Repository Implementations, DB
│         (Django ORM + PostgreSQL)      │
├─────────────────────────────────────────┤
│         CORE / DOMAIN LAYER            │  ← Entities, Interfaces (Pure Python)
│         (No Framework Dependencies)    │
└─────────────────────────────────────────┘
```

**Dependency Rule:** Layer luar boleh bergantung ke layer dalam, TIDAK sebaliknya.

---

## 🔐 JWT Authentication Flow

```
User Login → POST /auth/login/
          ← { access_token, refresh_token, user }

Request API → Header: Authorization: Bearer <access_token>
           ← Data response

Token Expired → POST /auth/token/refresh/
              ← { access: new_token }
```

---

## 📝 Contoh Request (curl)

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin1","email":"admin@test.com","password":"pass123","password_confirm":"pass123","role":"admin"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin1","password":"pass123"}'

# Dashboard Stats (dengan token)
curl http://localhost:8000/api/v1/auth/dashboard-stats/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
