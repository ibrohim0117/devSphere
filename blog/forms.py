from django import forms
from .models import Post



class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'tags', 'content', 'image', 'video', 'author']
        # widgets = {
        #     'tags': forms.SelectMultiple(attrs={'size': 5}),
        # }

    def clean(self):
        print(self.cleaned_data)
        return super().clean()


