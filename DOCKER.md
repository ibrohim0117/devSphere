# Docker Setup Guide

Bu loyiha Docker va Docker Compose yordamida ishga tushirish uchun tayyorlangan.

## Talablar

- Docker
- Docker Compose

## Tezkor boshlash

### 1. Environment faylini yaratish

`.env` faylini yarating va quyidagi o'zgaruvchilarni to'ldiring:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=devsphere_db
DB_USER=devsphere_user
DB_PASSWORD=devsphere_password
DB_HOST=db
DB_PORT=5432

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Social Login - Google
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Social Login - GitHub
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

### 2. Development muhitida ishga tushirish

```bash
# Containerlarni build qilish va ishga tushirish
docker-compose up --build

# Yoki backgroundda ishga tushirish
docker-compose up -d --build
```

### 3. Migrations va superuser yaratish

```bash
# Migrations qilish
docker-compose exec web python manage.py migrate

# Superuser yaratish
docker-compose exec web python manage.py createsuperuser

# Static fayllarni yig'ish
docker-compose exec web python manage.py collectstatic --noinput
```

### 4. Loyihani ochish

Brauzerda oching: http://localhost:8000

## Production muhitida ishga tushirish

### 1. Gunicorn qo'shish

`requirements.txt` ga qo'shing:
```
gunicorn==21.2.0
```

### 2. Production docker-compose ishlatish

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## Foydali buyruqlar

```bash
# Containerlarni to'xtatish
docker-compose down

# Containerlarni to'xtatish va volumelarni o'chirish
docker-compose down -v

# Loglarni ko'rish
docker-compose logs -f

# Faqat web servis loglarini ko'rish
docker-compose logs -f web

# Container ichiga kirish
docker-compose exec web bash

# Django shell
docker-compose exec web python manage.py shell

# Celery worker loglarini ko'rish
docker-compose logs -f celery

# Database backup
docker-compose exec db pg_dump -U devsphere_user devsphere_db > backup.sql

# Database restore
docker-compose exec -T db psql -U devsphere_user devsphere_db < backup.sql
```

## Servislar

- **web**: Django web application (port 8000)
- **db**: PostgreSQL database (port 5432)
- **redis**: Redis server (port 6379)
- **celery**: Celery worker
- **celery-beat**: Celery beat scheduler

## Muammolarni hal qilish

### Database connection xatosi

`.env` faylida `DB_HOST=db` ekanligini tekshiring.

### Static fayllar ko'rinmayapti

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Container qayta build qilish

```bash
docker-compose build --no-cache
docker-compose up -d
```
