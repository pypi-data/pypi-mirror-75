from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from djangosubscribe.models import WorkInformationModel
from djangosubscribe.modelforms import WorkInformationModelForm


class WorkInformationUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "djangoadmin/djangosubscribe/work_information_create_view.html"
    model = WorkInformationModel
    form_class = WorkInformationModelForm
    success_url = reverse_lazy("djangosubscribe:subscriber_list_view")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kwargs'] = self.kwargs.get("pk")
        return context