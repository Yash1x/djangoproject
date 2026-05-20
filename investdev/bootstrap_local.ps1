param(
    [switch]$CreateSuperuser
)

$ErrorActionPreference = "Stop"

Write-Host "==> Applying migrations..."
python manage.py migrate

python manage.py shell -c "from investdev_app.models import Publication; import sys; sys.exit(0 if Publication.objects.exists() else 1)" | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "==> Seed data already exists. Skipping loaddata."
} else {
    Write-Host "==> Loading seed data (investdev_app)..."
    python manage.py loaddata fixtures/investdev_app_seed.json
}

Write-Host "==> Running project checks..."
python manage.py check

if ($CreateSuperuser) {
    Write-Host "==> Creating superuser..."
    python manage.py createsuperuser
}

Write-Host "Done. Run: python manage.py runserver"
