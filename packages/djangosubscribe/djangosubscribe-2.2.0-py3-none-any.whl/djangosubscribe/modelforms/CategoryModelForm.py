from django import forms
from django.forms import ModelForm
from djangosubscribe.models.CategoryModel import CategoryModel


class CategoryModelForm(ModelForm):
    class Meta:
        model = CategoryModel
        fields = ['title', 'status']
        labels = {'title': 'Category name', 'status': 'Status'}

        help_texts = {
            "title": "Create unique category."
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Category'}),
            'status': forms.Select(attrs={'class': 'form-control rounded-0 mb-1'})
        }