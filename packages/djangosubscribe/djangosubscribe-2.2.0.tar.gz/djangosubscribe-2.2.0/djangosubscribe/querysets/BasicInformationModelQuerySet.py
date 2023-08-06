from django.db.models import QuerySet


class BasicInformationModelQuerySet(QuerySet):
    def author(self, user):
        return self.filter(author=user)