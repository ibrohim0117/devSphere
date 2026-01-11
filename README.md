# devSphere - Blog Platform

Django asosida yaratilgan to'liq funksionalli blog platformasi.

## ✨ Xususiyatlar

- 📝 Post yaratish, tahrirlash va o'chirish
- 📂 Kategoriyalar va Tag'lar boshqaruvi
- 👤 Foydalanuvchi profil boshqaruvi
- 💬 Izohlar va javoblar
- 😊 Emoji reaktsiyalar
- 🔍 Qidiruv va filtrlash
- 📧 Email tasdiqlash
- 🔐 Social login (Google, GitHub)
- ⚡ Celery orqali asinxron email yuborish
- 🎨 Responsive dizayn
- 🔧 Admin panel

## 🚀 O'rnatish

### Talablar

- Python 3.10+
- PostgreSQL (production uchun tavsiya etiladi)
- Redis (Celery uchun)

### 1. Repository'ni klon qiling

```bash
git clone <repository-url>
cd devSphere
```

### 2. Virtual environment yarating va faollashtiring

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

### 3. Kerakli paketlarni o'rnating

```bash
pip install -r requirements.txt
```

### 4. Environment variables sozlang

`.env.example` faylini `.env` ga ko'chiring va kerakli qiymatlarni kiriting:

```bash
cp .env.example .env
```

Keyin `.env` faylini tahrirlang:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
# ... boshqa sozlamalar
```

### 5. Database yarating va migratsiyalarni bajarish

```bash
python manage.py migrate
```

### 6. Superuser yarating (admin uchun)

```bash
python manage.py createsuperuser
```

### 7. Static fayllarni yig'ish (production uchun)

```bash
python manage.py collectstatic
```

### 8. Serverni ishga tushirish

```bash
# Development
python manage.py runserver

# Production uchun Gunicorn yoki uWSGI ishlatish tavsiya etiladi
gunicorn root.wsgi:application --bind 0.0.0.0:8000
```

### 9. Celery worker ishga tushirish (agar kerak bo'lsa)

```bash
celery -A root worker --loglevel=info
```

## 📦 Production Deployment

### Muhim sozlamalar

Production uchun `.env` faylida quyidagilarni o'rnating:

```env
DEBUG=False
SECRET_KEY=very-secure-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=devsphere_db
DB_USER=devsphere_user
DB_PASSWORD=secure-password
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis
REDIS_URL=redis://localhost:6379/0
```

### Security Checklist

Production'ga chiqarishdan oldin:

- ✅ `DEBUG=False` qiling
- ✅ `SECRET_KEY` ni xavfsiz qiling va hech qachon kodga commit qilmang
- ✅ `ALLOWED_HOSTS` ni to'g'ri sozlang
- ✅ `CSRF_TRUSTED_ORIGINS` ga HTTPS domain'laringizni qo'shing
- ✅ Database parolini xavfsiz qiling
- ✅ HTTPS ishlatishni ta'minlang
- ✅ Static files ni to'g'ri serve qiling (WhiteNoise yoki Nginx)
- ✅ Media files uchun xavfsiz yechim ishlating (CDN yoki Nginx)
- ✅ Celery worker ni systemd yoki supervisor orqali ishga tushiring
- ✅ Logging sozlang va monitoring qiling

### Static va Media Files

Production'da static va media files ni serve qilish uchun:

**Variant 1: WhiteNoise (Static files uchun)**

```bash
pip install whitenoise
```

`settings.py` da `MIDDLEWARE` ga qo'shing:

```python
MIDDLEWARE = [
    # ...
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # SecurityMiddleware dan keyin
    # ...
]
```

**Variant 2: Nginx (Tavsiya etiladi)**

Nginx konfiguratsiyasi:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location /static/ {
        alias /path/to/devSphere/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/devSphere/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🛠️ Development

### Migration yaratish

```bash
python manage.py makemigrations
python manage.py migrate
```

### Static files ishlab chiqish

```bash
python manage.py collectstatic --noinput
```

### Test ishga tushirish

```bash
python manage.py test
```

## 📝 Struktura

```
devSphere/
├── blog/           # Blog app
├── users/          # Users app
├── root/           # Project settings
├── templates/      # HTML templates
├── static/         # Static files (CSS, JS, images)
├── media/          # Media files (user uploads)
├── logs/           # Log files
└── manage.py
```

## 🔧 Xizmatlar

### Admin Panel

- URL: `/admin/`
- Category boshqaruvi: `/blog/admin/categories/`
- Tag boshqaruvi: `/blog/admin/tags/`
- Post boshqaruvi: `/blog/admin/posts/`

### API Endpoints

- Home: `/blog/`
- Post detail: `/blog/post/<slug>/`
- User profile: `/user/profile/`
- Login: `/user/login/`
- Register: `/user/register/`

## 📄 License

Bu loyiha shaxsiy foydalanish uchun yaratilgan.

## 🤝 Yordam

Muammo yoki savol bo'lsa, issue yarating yoki email orqali bog'laning.
