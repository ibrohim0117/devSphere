# Ngrok Configuration - Global Test

## Ngrok Status
✅ Ngrok ishlamoqda va global test uchun tayyor!

## Current Ngrok URL
**Public URL:** `https://1e2083b916c7.ngrok-free.app`

## Django Server
- **Local URL:** `http://127.0.0.1:8000`
- **Status:** ✅ Ishlamoqda

## Ngrok Configuration
- **Port:** 8000
- **Web Interface:** `http://127.0.0.1:4040`

## Important Notes

1. **Ngrok Warning Page:**
   - Birinchi marta kirganda ngrok "Visit Site" tugmasini bosish kerak
   - Bu ngrok'ning xavfsizlik xususiyati

2. **CSRF Settings:**
   - Settings.py avtomatik ngrok URL'ni CSRF_TRUSTED_ORIGINS ga qo'shadi
   - Ngrok API orqali URL o'qiladi: `http://127.0.0.1:4040/api/tunnels`

3. **Restart Server:**
   - Agar ngrok URL o'zgarsa, Django serverni qayta ishga tushirish kerak
   - Yoki settings.py avtomatik yangi URL'ni topadi (agar ngrok ishlamoqda bo'lsa)

## Commands

### Django Serverni to'xtatish:
```bash
pkill -f "manage.py runserver"
```

### Ngrok'ni to'xtatish:
```bash
pkill -f ngrok
```

### Django Server va Ngrok'ni qayta ishga tushirish:
```bash
# 1. Django serverni background'da ishga tushirish
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000 &

# 2. Ngrok'ni background'da ishga tushirish
ngrok http 8000 &

# 3. Ngrok URL'ni olish
curl -s http://127.0.0.1:4040/api/tunnels | python3 -m json.tool
```

## Access URLs

- **Home Page:** `https://1e2083b916c7.ngrok-free.app/blog/`
- **Admin Panel:** `https://1e2083b916c7.ngrok-free.app/admin/`
- **Register:** `https://1e2083b916c7.ngrok-free.app/user/register/`
- **Login:** `https://1e2083b916c7.ngrok-free.app/user/login/`

## Security Notes

⚠️ **Bu faqat test uchun!** Production'da ngrok ishlatmang!
- Ngrok free plan'da URL har safar o'zgaradi
- Production uchun to'g'ri domain va SSL sertifikat ishlating
