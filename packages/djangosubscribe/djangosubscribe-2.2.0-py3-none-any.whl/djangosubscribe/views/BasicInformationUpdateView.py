from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from djangosubscribe.models import BasicInformationModel
from djangosubscribe.modelforms import BasicInformationModelForm


class BasicInformationUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "djangoadmin/djangosubscribe/basic_information_create_view.html"
    form_class = BasicInformationModelForm
    model = BasicInformationModel
    success_message = "basic information updated successfully."

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect("djangosubscribe:parental_information_update_view", pk=form.instance.pk)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kwargs'] = self.kwargs['pk']
        return context