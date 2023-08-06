from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from djangosubscribe.managers import CategoryModelManager


class CategoryModel(models.Model):
    STATUS_CHOICES = (('ACTIVE', 'Active'), ('DEACTIVE', 'Deactive'))
    title          = models.CharField(max_length=15)
    slug           = models.SlugField(max_length=18)
    status         = models.CharField(max_length=8, choices=STATUS_CHOICES, default='Active')
    author         = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    objects        = CategoryModelManager()

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['-pk']

    def save(self, *args, **kwargs):
        if self.title:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def get_absolute_update_url(self, **kwargs):
        return reverse("djangosubscribe:category_update_view", kwargs={'category_pk': self.pk})

    def get_absolute_delete_url(self, **kwargs):
        return reverse("djangosubscribe:category_delete_view", kwargs={'category_pk': self.pk})