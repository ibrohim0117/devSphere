import uuid
from django.views.generic import TemplateView, FormView, UpdateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegisterForm, UserLoginForm
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
    def get(self, request, token, *args, **kwargs):
        try:
            confirmation = EmailConfirmation.objects.get(token=token)
        except EmailConfirmation.DoesNotExist:
            return HttpResponse("Noto'g'ri yoki muddati o'tgan tasdiqlash linki.", status=400)

        user = confirmation.user
        user.is_active = True
        user.is_verified = True
        user.save()

        # confirmation.delete()

        login(request, user)

        messages.success(request, "Email muvaffaqiyatli tasdiqlandi va siz tizimga kirdingiz!")
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
            login(self.request, user)
            return redirect('home')
        return super().form_valid(form)


class LogoutRedirectView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('home')



class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'profile.html'
    fields = [
        'avatar', 'about', 'email', 'facebook', 'twitter',
        'instagram', 'linkedin', 'github', 'leetcode',
        'telegram'
    ]
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profil muvaffaqiyatli yangilandi!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Xatolik: iltimos ma\'lumotlarni to‘g‘ri to‘ldiring.')
        return super().form_invalid(form)

