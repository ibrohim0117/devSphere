from django.db import models
from django.utils.text import slugify

class BaseCreatedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class Category(BaseCreatedModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
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
    content = models.TextField()
    views = models.PositiveIntegerField(default=0, editable=False)
    imoji = models.ForeignKey(Emoji, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')

