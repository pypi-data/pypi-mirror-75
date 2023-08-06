from django.db import models
from django.contrib.auth.models import User
from djangosubscribe.models import QuickEmailSubscriptionModel
from djangosubscribe.models.CategoryModel import CategoryModel


class WorkInformationModel(models.Model):
    STATUS_CHOICES = (('ACTIVE', 'active'), ('DEACTIVE', 'deactive'))
    username       = models.CharField(max_length=15, null=True, blank=True)
    email          = models.ForeignKey(QuickEmailSubscriptionModel, on_delete=models.CASCADE)
    category       = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    status         = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    work           = models.CharField(max_length=180, null=True, blank=True)
    profession     = models.CharField(max_length=180, null=True, blank=True)
    author         = models.ForeignKey(User, on_delete=models.CASCADE)
    status         = models.CharField(max_length=8, choices=STATUS_CHOICES)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Work Information"
        verbose_name_plural = "Work Informations"
        ordering = ['-pk']