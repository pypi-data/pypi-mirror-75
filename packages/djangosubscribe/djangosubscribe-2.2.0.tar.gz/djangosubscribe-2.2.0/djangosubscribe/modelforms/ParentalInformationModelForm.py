from django import forms
from django.forms import ModelForm
from djangosubscribe.models import ParentalInformationModel


class ParentalInformationModelForm(ModelForm):
    class Meta:
        model = ParentalInformationModel

        fields = ['father', 'father_mobile', 'father_occupation',
                  'mother', 'mother_mobile', 'mother_occupation', 'status'
        ]

        labels = {
            "father": "Father's name",
            "father_mobile": "Father's mobile",
            "father_occupation": "Father's occupation",
            "mother": "Mother's name",
            "mother_mobile": "Mother's mobile",
            "mother_occupation": "Mother's occupation",
            "status": "Status"
        }

        widgets = {
            "father": forms.TextInput(attrs={'type':'text', 'class':'form-control rounded-0 mb-1', 'placeholder':"Father's name"}),
            "father_mobile": forms.NumberInput(attrs={'type':'number', 'class':'form-control rounded-0 mb-1', 'placeholder':"Father's mobile"}),
            "father_occupation": forms.TextInput(attrs={'type':'text', 'class':'form-control rounded-0 mb-1', 'placeholder':"Father's occupation"}),
            "mother": forms.TextInput(attrs={'type':'text', 'class':'form-control rounded-0 mb-1', 'placeholder':"Mother's name"}),
            "mother_mobile": forms.NumberInput(attrs={'type':'number', 'class':'form-control rounded-0 mb-1', 'placeholder':"Mother's mobile"}),
            "mother_occupation": forms.TextInput(attrs={'type':'text', 'class':'form-control rounded-0 mb-1', 'placeholder':"Mother's occupation"}),
            "status": forms.Select(attrs={'class':'form-control rounded-0 mb-1'})
        }