from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from djangosubscribe.models import CategoryModel
from djangosubscribe.modelforms import CategoryModelForm


# Create your views here.
class CategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "djangoadmin/djangosubscribe/category_create_view.html"
    model = CategoryModel
    form_class = CategoryModelForm
    success_url = reverse_lazy("djangosubscribe:category_list_view")
    success_message = "category created successfully."

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_message(self, cleaned_data):
        return f"{cleaned_data['title']} {self.success_message}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_form'] = context['form']
        return context