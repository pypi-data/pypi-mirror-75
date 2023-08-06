from django import forms
from django.forms import ModelForm
from djangosubscribe.models import QuickEmailSubscriptionModel


class OverviewModelForm(ModelForm):
    class Meta:
        model = QuickEmailSubscriptionModel
        fields = ['username', 'email', 'mobile', 'category', 'status']
        labels = {'username':'User Name', 'email':'Email', 'mobile': 'Mobile no.', 'category':'Category', 'status':'Status'}

        help_texts = {
            "username": "Create an unique user name, it required 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
            "email": "Email address must be unique.",
            "mobile": "Mobile number must be unique."
        }

        widgets = {
            'username': forms.TextInput(attrs={'type':'text', 'class':'form-control rounded-0', 'placeholder':'User name'}),
            'email': forms.EmailInput(attrs={'type':'email', 'class':'form-control rounded-0', 'placeholder':'Email'}),
            'mobile': forms.NumberInput(attrs={'type':'number', 'class':'form-control rounded-0', 'placeholder':'Mobile no.'}),
            'category': forms.Select(attrs={'class':'form-control rounded-0'}),
            'status': forms.Select(attrs={'class':'form-control rounded-0 mb-1'})
        }