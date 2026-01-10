from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'tags', 'content', 'image', 'video']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post sarlavhasi'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control', 'size': 5}),
            'content': CKEditorWidget(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'video': forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or len(title.strip()) < 5:
            raise forms.ValidationError('Sarlavha kamida 5 ta belgidan iborat bo\'lishi kerak')
        return title.strip()

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or len(content.strip()) < 20:
            raise forms.ValidationError('Kontent kamida 20 ta belgidan iborat bo\'lishi kerak')
        return content

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')
        
        # Yangi post yaratganda kamida bitta rasm yoki video kerak
        # Tahrirlashda esa mavjud fayllar bo'lsa, yangi fayl qo'shish ixtiyoriy
        if not self.instance.pk:  # Yangi post
            if not image and not video:
                raise forms.ValidationError('Kamida bitta rasm yoki video qo\'shishingiz kerak')
        else:  # Tahrirlash
            # Agar yangi fayl qo'shilmagan bo'lsa, mavjud fayllarni tekshirish
            if not image and not video:
                if not self.instance.image and not self.instance.video:
                    raise forms.ValidationError('Kamida bitta rasm yoki video qo\'shishingiz kerak')
        
        return cleaned_data


