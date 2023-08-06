from django import forms
from django.forms import ModelForm
from djangosubscribe.models import BasicInformationModel


class BasicInformationModelForm(ModelForm):
    class Meta:
        model = BasicInformationModel

        fields = ['first_name', 'last_name', 'birthday', 'image', 'gender', 'language',
                  'religion', 'politics', 'status']

        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'birthday': 'Birthday',
            'image': 'Image',
            'gender': 'Gender',
            'language': 'Language',
            'religion': 'Religion',
            'politics': 'Politics',
            'status': 'Status'
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'type':'text', 'class':'rounded-0 form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'type':'text', 'class':'rounded-0 form-control', 'placeholder': 'Last Name'}),
            'birthday': forms.DateInput(attrs={'type':'text', 'id':'datepicker', 'class':'rounded-0 form-control', 'placeholder':'Pick a date'}),
            'image': forms.ClearableFileInput(attrs={'type':'file', 'class':'form-control-file runded-0'}),
            'gender': forms.Select(attrs={'type':'text', 'class':'rounded-0 form-control', 'placeholder': 'Gender'}),
            'language': forms.TextInput(attrs={'type':'text', 'class':'rounded-0 form-control', 'placeholder': 'Language'}),
            'religion': forms.TextInput(attrs={'type':'text', 'class':'rounded-0 form-control', 'placeholder': 'Religion'}),
            'politics': forms.TextInput(attrs={'type':'text', 'class':'rounded-0 form-control', 'placeholder': 'Politics'}),
            'status': forms.Select(attrs={'class':'form-control rounded-0 mb-1'})
        }