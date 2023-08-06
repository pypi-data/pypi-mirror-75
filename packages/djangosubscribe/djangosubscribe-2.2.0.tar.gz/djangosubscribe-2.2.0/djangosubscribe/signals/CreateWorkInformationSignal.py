from django.db.models.signals import post_save
from djangosubscribe.models import WorkInformationModel
from djangosubscribe.models import QuickEmailSubscriptionModel


def CreateWorkInformationSignal(sender, instance, created, **kwargs):
    if created:
        i = instance
        WorkInformationModel.objects.create(email=i,username=i.username,status=i.status,category=i.category,author=i.author)
post_save.connect(CreateWorkInformationSignal, sender=QuickEmailSubscriptionModel)