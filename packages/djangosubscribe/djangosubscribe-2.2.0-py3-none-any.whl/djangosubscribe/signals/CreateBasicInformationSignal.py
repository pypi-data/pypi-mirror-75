from django.db.models.signals import post_save
from djangosubscribe.models import BasicInformationModel
from djangosubscribe.models import QuickEmailSubscriptionModel


def CreateBasicInformationSignal(sender, created, instance, **kwargs):
    if created:
        i = instance
        BasicInformationModel.objects.create(email=i,username=i.username,status=i.status,category=i.category,author=i.author)
post_save.connect(CreateBasicInformationSignal, sender=QuickEmailSubscriptionModel)