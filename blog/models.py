from django.db import models
from django.utils.text import slugify
from ckeditor import fields
from root import settings
from django_resized import ResizedImageField
from datetime import timedelta
from django.db.models import Count



class BaseCreatedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class Category(BaseCreatedModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
            # Agar slug allaqachon mavjud bo'lsa, raqam qo'shish
            original_slug = self.slug
            counter = 1
            while Category.objects.filter(slug=self.slug).exclude(pk=self.pk if self.pk else None).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(BaseCreatedModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Emoji(BaseCreatedModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(BaseCreatedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    content = fields.RichTextField()
    image = models.ImageField(upload_to='posts/images/%Y/%m/%d', null=True, blank=True)
    video = models.FileField(upload_to='posts/video/%Y/%m/%d', null=True, blank=True)
    views = models.PositiveIntegerField(default=0, editable=False)
    tags = models.ManyToManyField(Tag, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


    @property
    def created_at_plus_5(self):
        return self.created_at + timedelta(hours=5)

    @property
    def emoji_set_list(self):
        return self.reactions.values('emoji').annotate(count=Count('id'))

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.title):
            self.slug = slugify(self.title)
            # Agar slug allaqachon mavjud bo'lsa, raqam qo'shish
            original_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exclude(pk=self.pk if self.pk else None).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)




class Reaction(models.Model):
    EMOJI_CHOICES = [
        ('👍', 'Like'),
        ('❤️', 'Love'),
        ('😂', 'Laugh'),
        ('🔥', 'Fire'),
        ('😮', 'Wow'),
        ('😢', 'Sad'),
        ('👏', 'Clap'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    emoji = models.CharField(max_length=5, choices=EMOJI_CHOICES)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'ip_address')

    def __str__(self):
        return f"{self.emoji}"


class Comment(BaseCreatedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=1000)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def created_at_plus_5(self):
        return self.created_at + timedelta(hours=5)

    def __str__(self):
        return f"Comment by {self.author.email} on {self.post.title}"



