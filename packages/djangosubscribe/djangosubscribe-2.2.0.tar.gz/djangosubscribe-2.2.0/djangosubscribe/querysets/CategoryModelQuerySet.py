from django.db.models import QuerySet


class CategoryModelQuerySet(QuerySet):
    def author(self, user):
        return self.filter(author=user)