from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
from django.contrib import messages
from django.contrib.messages import add_message
from django.urls import reverse_lazy
from djangosubscribe.models import QuickEmailSubscriptionModel


class SubscriberDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "djangoadmin/djangosubscribe/subscriber_delete_view.html"
    model = QuickEmailSubscriptionModel
    success_url = reverse_lazy("djangosubscribe:subscriber_list_view")
    context_object_name = "subscriber_detail"
    success_message = "subscriber deleted successfully."

    def delete(self, request, *args, **kwargs):
        instance = QuickEmailSubscriptionModel.objects.get(pk=self.kwargs['pk'])
        message = f"\"{instance.username}\" {self.success_message}"
        add_message(self.request, messages.SUCCESS, message, extra_tags="success")
        return super().delete(request, *args, **kwargs)