from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.shortcuts import redirect
from djangosubscribe.models import ParentalInformationModel
from djangosubscribe.modelforms import ParentalInformationModelForm


class ParentalInformationUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "djangoadmin/djangosubscribe/parental_information_create_view.html"
    form_class = ParentalInformationModelForm
    model = ParentalInformationModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kwargs'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect("djangosubscribe:educational_information_update_view", pk=form.instance.pk)

    def form_invalid(self, form):
        return super().form_valid(form)