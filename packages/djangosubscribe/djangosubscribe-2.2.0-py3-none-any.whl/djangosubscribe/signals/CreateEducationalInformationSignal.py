from django.db.models.signals import post_save
from djangosubscribe.models import QuickEmailSubscriptionModel
from djangosubscribe.models import EducationalInformationModel


def CreateEducationalInformationSignal(sender, instance, created, **kwargs):
    if created:
        i = instance
        EducationalInformationModel.objects.create(email=i,username=i.username,status=i.status,category=i.category,author=i.author)
post_save.connect(CreateEducationalInformationSignal, sender=QuickEmailSubscriptionModel)