from django import forms
from .models import User



class RegisterForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu email allaqachon ro'yxatdan o'tgan.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Parollar mos emas.")
        return cleaned_data


class UserLoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):
    """Profilni yangilash uchun form. Email maydoni yo'q."""
    class Meta:
        model = User
        fields = [
            'avatar', 'about', 'facebook', 'twitter',
            'instagram', 'linkedin', 'github', 'leetcode',
            'telegram'
        ]
        widgets = {
            'about': forms.Textarea(attrs={
                'placeholder': "O'zingiz haqingizda yozing...",
                'rows': 5
            }),
            'facebook': forms.URLInput(attrs={'placeholder': 'https://facebook.com/...'}),
            'twitter': forms.URLInput(attrs={'placeholder': 'https://twitter.com/...'}),
            'instagram': forms.URLInput(attrs={'placeholder': 'https://instagram.com/...'}),
            'linkedin': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/...'}),
            'github': forms.URLInput(attrs={'placeholder': 'https://github.com/...'}),
            'leetcode': forms.URLInput(attrs={'placeholder': 'https://leetcode.com/...'}),
            'telegram': forms.URLInput(attrs={'placeholder': 'https://t.me/...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Barcha maydonlarni ixtiyoriy qilish
        for field_name, field in self.fields.items():
            field.required = False
            if field_name == 'avatar':
                field.widget.attrs.update({
                    'accept': 'image/*',
                })