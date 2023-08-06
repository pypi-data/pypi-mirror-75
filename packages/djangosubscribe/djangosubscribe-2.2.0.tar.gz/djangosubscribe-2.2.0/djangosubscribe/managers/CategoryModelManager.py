from django.db.models import Manager
from djangosubscribe.querysets import CategoryModelQuerySet


class CategoryModelManager(Manager):
    def get_queryset(self):
        return CategoryModelQuerySet(self.model, using=self._db)

    def author(self, user):
        return self.get_queryset().author(user)