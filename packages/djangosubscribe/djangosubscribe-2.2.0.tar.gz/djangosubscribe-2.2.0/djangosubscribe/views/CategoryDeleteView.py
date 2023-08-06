from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from djangosubscribe.models import CategoryModel


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "djangoadmin/djangosubscribe/category_delete_view.html"
    model = CategoryModel
    pk_url_kwarg = "category_pk"
    success_url = reverse_lazy("djangosubscribe:category_list_view")
    context_object_name = "category_detail"
    success_message = "category deleted successfully."

    def delete(self, request, *args, **kwargs):
        success_message = f"{self.success_message}"
        messages.success(self.request, success_message, extra_tags='warning')
        return super().delete(request, *args, **kwargs)