from django.db.models import Manager
from djangosubscribe.querysets import QuickEmailSubscriptionModelQuerySet


class QuickEmailSubscripionModelManager(Manager):
    def get_queryset(self):
        return QuickEmailSubscriptionModelQuerySet(self.model, using=self._db)

    def author(self, user):
        return self.get_queryset().author(user)