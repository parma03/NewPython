# ============================================================
# AppSystem - Single Run Script (Windows PowerShell)
# Jalankan: .\run.ps1
# ============================================================

$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
$BACKEND = Join-Path $ROOT "backend"
$FRONTEND = Join-Path $ROOT "frontend"

Write-Host ""
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "      AppSystem - Starting All Services       " -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

# ── Cek virtual environment ─────────────────────────────────
$VENV_PYTHON = Join-Path $BACKEND "venv\Scripts\python.exe"

if (-Not (Test-Path $VENV_PYTHON)) {
    Write-Host "[ERROR] Virtual environment tidak ditemukan." -ForegroundColor Red
    Write-Host "Jalankan setup dulu:" -ForegroundColor Yellow
    Write-Host "  cd backend"
    Write-Host "  python -m venv venv"
    Write-Host "  venv\Scripts\activate"
    Write-Host "  pip install -r requirements.txt"
    exit 1
}

Write-Host "[OK] Virtual environment ditemukan" -ForegroundColor Green

# ── Start Backend ───────────────────────────────────────────
Write-Host "[INFO] Starting Backend  : http://localhost:8000" -ForegroundColor Blue

Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$BACKEND'; Write-Host '=== BACKEND ===' -ForegroundColor Blue; .\venv\Scripts\activate; python manage.py runserver"
)

Start-Sleep -Seconds 2

# ── Start Frontend ──────────────────────────────────────────
Write-Host "[INFO] Starting Frontend : http://localhost:5500" -ForegroundColor Green

Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$FRONTEND'; Write-Host '=== FRONTEND ===' -ForegroundColor Green; python -m http.server 5500"
)

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "[SUCCESS] Semua service berjalan!" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend : http://localhost:5500" -ForegroundColor Cyan
Write-Host "Backend  : http://localhost:8000/api/v1/" -ForegroundColor Cyan
Write-Host ""

Start-Process "http://localhost:5500"