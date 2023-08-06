from django import forms
from django.forms import ModelForm
from djangosubscribe.models import EducationalInformationModel


class EducationalInformationModelForm(ModelForm):
    class Meta:
        model = EducationalInformationModel
        fields = ["high_school", "university", "status"]

        labels = {
            "high_school": "High school",
            "university": "University",
        }

        widgets = {
            'high_school': forms.TextInput(attrs={'type':'text', 'class':'rounded-0 form-control', 'placeholder': 'High school'}),
            'university': forms.TextInput(attrs={'type':'text', 'class':'rounded-0 form-control', 'placeholder': 'University'}),
            'status': forms.Select(attrs={'class':'form-control rounded-0 mb-1'})
        }