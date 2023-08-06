from django.db.models.signals import post_save
from djangosubscribe.models import ParentalInformationModel
from djangosubscribe.models import QuickEmailSubscriptionModel


def CreateParentalInformationSignal(sender, instance, created, **kwargs):
    if created:
        i = instance
        ParentalInformationModel.objects.create(email=i,username=i.username,status=i.status,category=i.category,author=i.author)
post_save.connect(CreateParentalInformationSignal, sender=QuickEmailSubscriptionModel)