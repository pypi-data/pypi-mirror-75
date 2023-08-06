from django.db.models import QuerySet


class QuickEmailSubscriptionModelQuerySet(QuerySet):
    def author(self, user):
        return self.filter(author=user)