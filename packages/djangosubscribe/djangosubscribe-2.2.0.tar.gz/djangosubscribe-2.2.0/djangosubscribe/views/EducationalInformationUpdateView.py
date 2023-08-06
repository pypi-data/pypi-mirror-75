from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from djangosubscribe.models import EducationalInformationModel
from djangosubscribe.modelforms import EducationalInformationModelForm


class EducationalInformationUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "djangoadmin/djangosubscribe/educational_information_create_view.html"
    model = EducationalInformationModel
    form_class = EducationalInformationModelForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect("djangosubscribe:work_information_update_view", pk=form.instance.pk)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kwargs'] = self.kwargs.get("pk")
        return context