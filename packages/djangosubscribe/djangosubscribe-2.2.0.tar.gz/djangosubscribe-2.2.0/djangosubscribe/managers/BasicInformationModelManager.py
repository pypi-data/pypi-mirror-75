from django.db.models import Manager
from djangosubscribe.querysets import BasicInformationModelQuerySet


class BasicInformationModelManager(Manager):
    def get_queryset(self):
        return BasicInformationModelQuerySet(self.model, using=self._db)

    def author(self, user):
        return self.get_queryset().author(user)