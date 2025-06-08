from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.http import HttpResponse
from django.contrib.auth import login

from .forms import RegisterForm
from .tasks import send_verification_email
from .models import User, EmailConfirmation
import uuid



class RegisterView(TemplateView):
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

        # return HttpResponse("Email muvaffaqiyatli tasdiqlandi. Endi tizimga kirishingiz mumkin.")

