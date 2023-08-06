from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from djangosubscribe.models import QuickEmailSubscriptionModel
from djangosubscribe.modelforms import OverviewModelForm


class SubscriberUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "djangoadmin/djangosubscribe/subscriber_create_view.html"
    model = QuickEmailSubscriptionModel
    form_class = OverviewModelForm
    success_url = reverse_lazy("djangosubscribe:subscriber_list_view")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['overviewform'] = context['form']
        context['kwargs'] = self.kwargs['pk']
        return context