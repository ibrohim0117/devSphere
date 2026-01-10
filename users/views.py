import uuid
from django.views.generic import TemplateView, FormView, UpdateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegisterForm, UserLoginForm, ProfileForm, ResendVerificationEmailForm
from .tasks import send_verification_email
from .models import User, EmailConfirmation
from .mixins import NotLoginRequiredMixin



class RegisterView(NotLoginRequiredMixin, TemplateView):
    template_name = 'register.html'

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(
                email=email,
                password=password,
                is_active=False
            )

            token = uuid.uuid4()
            EmailConfirmation.objects.create(user=user, token=token)

            verification_link = request.build_absolute_uri(
                reverse('verify-email', kwargs={'token': str(token)})
            )

            send_verification_email.delay(
                subject='Tasdiqlash havolasi',
                message=f"Iltimos, emailingizni tasdiqlang: {verification_link}",
                from_email='ibrohim.dev.uz@gmail.com',
                recipient_list=[email]
            )

            messages.success(request, "Ro'yxatdan o'tish muvaffaqiyatli. Iltimos, emailingizni tekshiring.")
            return redirect(reverse('register'))
        return render(request, self.template_name, {'form': form})



class VerifyEmailView(View):
    """Email tasdiqlash uchun class-based view"""
    
    def get(self, request, token, *args, **kwargs):
        try:
            confirmation = EmailConfirmation.objects.get(token=token)
        except EmailConfirmation.DoesNotExist:
            messages.error(
                request, 
                "❌ Noto'g'ri tasdiqlash linki. Agar linkning muddati o'tgan bo'lsa, "
                "yangi link olish uchun emailingizni kiriting."
            )
            return redirect('resend_verification')

        # Token muddatini tekshirish
        if confirmation.is_expired():
            user_email = confirmation.user.email
            confirmation.delete()
            messages.warning(
                request, 
                f"⏰ Tasdiqlash linki muddati o'tgan. Link faqat 24 soat davomida amal qiladi. "
                f"Yangi link olish uchun emailingizni kiriting."
            )
            # Yangi link olish sahifasiga redirect qilish, email parametr bilan
            return redirect(f"{reverse('resend_verification')}?email={user_email}")

        user = confirmation.user
        
        # Agar allaqachon tasdiqlangan bo'lsa
        if user.is_verified and user.is_active:
            messages.info(request, "ℹ️ Email allaqachon tasdiqlangan. Tizimga kirildi.")
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')

        user.is_active = True
        user.is_verified = True
        user.save()

        # Token'ni o'chirish
        confirmation.delete()

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        messages.success(request, "✅ Email muvaffaqiyatli tasdiqlandi va siz tizimga kirdingiz!")
        return redirect('home')



class UserLoginView(NotLoginRequiredMixin, FormView):
    form_class = UserLoginForm
    template_name = 'login.html'
    success_url = 'home'

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = User.objects.filter(email=email).first()
        
        if user and user.check_password(password):
            # Superuser har doim login qila oladi
            if not user.is_active and not user.is_superuser:
                messages.error(self.request, "Hisobingiz faol emas. Iltimos, emailingizni tasdiqlang.")
                return redirect('login')
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(self.request, f"Xush kelibsiz, {user.email}!")
            return redirect('home')
        else:
            messages.error(self.request, "Email yoki parol noto'g'ri.")
            return super().form_invalid(form)


class LogoutRedirectView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('home')



class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'profile.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        # Email o'zgartirilmasligini ta'minlash
        form.instance.email = self.request.user.email
        messages.success(self.request, 'Profil muvaffaqiyatli yangilandi!')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Form xatolarini ko'rsatish
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field}: {error}')
        return super().form_invalid(form)


class ResendVerificationEmailView(NotLoginRequiredMixin, FormView):
    """Yangi tasdiqlash linkini yuborish uchun class-based view"""
    form_class = ResendVerificationEmailForm
    template_name = 'resend_verification.html'
    success_url = reverse_lazy('login')
    
    def get_initial(self):
        """GET parametrdan email parametrini olish"""
        initial = super().get_initial()
        email = self.request.GET.get('email')
        if email:
            initial['email'] = email
        return initial
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        
        # Eski tokenlarni o'chirish (expired yoki faol)
        EmailConfirmation.objects.filter(user=user).delete()
        
        # Yangi token yaratish
        token = uuid.uuid4()
        EmailConfirmation.objects.create(user=user, token=token)
        
        # Yangi tasdiqlash linkini yuborish
        verification_link = self.request.build_absolute_uri(
            reverse('verify-email', kwargs={'token': str(token)})
        )
        
        send_verification_email.delay(
            subject='Yangi tasdiqlash havolasi - devSphere',
            message=f"Yangi tasdiqlash havolasi:\n{verification_link}\n\nBu link 24 soat davomida amal qiladi.",
            from_email='ibrohim.dev.uz@gmail.com',
            recipient_list=[email]
        )
        
        messages.success(
            self.request, 
            f"✅ Yangi tasdiqlash linki {email} manziliga yuborildi! "
            f"Iltimos, emailingizni tekshiring. Link 24 soat davomida amal qiladi."
        )
        return super().form_valid(form)

