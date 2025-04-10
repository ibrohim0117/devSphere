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