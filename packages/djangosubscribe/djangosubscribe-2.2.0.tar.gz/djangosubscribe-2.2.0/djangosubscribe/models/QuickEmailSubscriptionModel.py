from django.db import models
from django.contrib.auth.models import User
from djangosubscribe.models.CategoryModel import CategoryModel
from djangosubscribe.managers import QuickEmailSubscripionModelManager


class QuickEmailSubscriptionModel(models.Model):
    STATUS_CHOICES = (('ACTIVE', 'active'), ('DEACTIVE', 'deactive'))
    username   = models.CharField(max_length=15, null=True, blank=True)
    email      = models.EmailField(max_length=75, blank=False, null=False)
    mobile     = models.BigIntegerField(null=True, blank=True)
    category   = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, default='3')
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    status     = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects    = QuickEmailSubscripionModelManager()

    class Meta:
        verbose_name = "Quick Email Subsciption"
        verbose_name_plural = "Quick Email Subscriptions"
        ordering = ["-pk"]

    def __str__(self):
        return f"{self.email}"