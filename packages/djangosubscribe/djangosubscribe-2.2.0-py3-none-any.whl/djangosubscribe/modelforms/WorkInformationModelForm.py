from django import forms
from django.forms import ModelForm
from djangosubscribe.models import WorkInformationModel


class WorkInformationModelForm(ModelForm):
    class Meta:
        model = WorkInformationModel
        fields = ["work", "profession", "status"]

        labels = {
            "work": "Work",
            "profession": "Profession",
            "status": "Status"
        }

        widgets = {
            'work': forms.TextInput(attrs={'type':'text', 'class':'rounded-0 form-control', 'placeholder': 'Work'}),
            'profession': forms.TextInput(attrs={'type':'text', 'class':'rounded-0 form-control', 'placeholder': 'Profession'}),
            'status': forms.Select(attrs={'class':'form-control rounded-0 mb-1'})
        }