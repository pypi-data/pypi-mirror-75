from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from djangosubscribe.modelforms import OverviewModelForm


class SubscriberCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "djangoadmin/djangosubscribe/subscriber_create_view.html"
    form_class = OverviewModelForm
    success_message = "subscriber created successfully."

    def get_success_message(self, cleaned_data):
        return self.success_message

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect("djangosubscribe:basic_information_update_view", pk=form.instance.pk)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['overviewform'] = context['form']
        return context