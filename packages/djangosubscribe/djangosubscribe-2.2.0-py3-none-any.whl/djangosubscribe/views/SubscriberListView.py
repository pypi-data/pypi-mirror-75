from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from djangosubscribe.models import BasicInformationModel


class SubscriberListView(LoginRequiredMixin, ListView):
    template_name = "djangoadmin/djangosubscribe/subscriber_list_view.html"
    context_object_name = "subscriber_list"

    def get_queryset(self):
        return BasicInformationModel.objects.author(self.request.user)