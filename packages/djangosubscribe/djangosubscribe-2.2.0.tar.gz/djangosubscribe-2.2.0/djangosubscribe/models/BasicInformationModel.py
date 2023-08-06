from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from djangosubscribe.models import QuickEmailSubscriptionModel
from djangosubscribe.models.CategoryModel import CategoryModel
from djangosubscribe.managers import BasicInformationModelManager


class BasicInformationModel(models.Model):
    STATUS_CHOICES = (('ACTIVE', 'active'), ('DEACTIVE', 'deactive'))
    GENDER_CHOICES = (('MALE', 'Male'), ('FEMALE', 'Female'), ('CUSTOM', 'Custom'))
    username       = models.CharField(max_length=15, null=True, blank=True)
    first_name     = models.CharField(max_length=15, null=True, blank=True)
    last_name      = models.CharField(max_length=15, null=True, blank=True)
    email          = models.ForeignKey(QuickEmailSubscriptionModel, on_delete=models.CASCADE)
    category       = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    status         = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    birthday       = models.DateField(null=True, blank=True)
    image          = models.ImageField(null=True, blank=True)
    gender         = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    language       = models.CharField(max_length=20, null=True, blank=True)
    religion       = models.CharField(max_length=20, null=True, blank=True)
    politics       = models.CharField(max_length=20, null=True, blank=True)
    author         = models.ForeignKey(User, on_delete=models.CASCADE)
    status         = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active', null=True, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    objects        = BasicInformationModelManager()

    class Meta:
        verbose_name = "Basic Information"
        verbose_name_plural = "Basic Informations"
        ordering = ["-pk"]

    def get_absolute_update_url(self, **kwargs):
        return reverse("djangosubscribe:subscriber_update_view", kwargs={'pk': self.pk})

    def get_absolute_delete_url(self, **kwargs):
        return reverse("djangosubscribe:subscriber_delete_view", kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.email}"