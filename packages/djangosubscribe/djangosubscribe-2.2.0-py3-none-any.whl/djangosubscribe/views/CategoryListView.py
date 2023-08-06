from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from djangosubscribe.models import CategoryModel


# Create your views here.
class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "djangoadmin/djangosubscribe/category_list_view.html"
    context_object_name = "category_list"

    def get_queryset(self):
        return CategoryModel.objects.author(self.request.user)