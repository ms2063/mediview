from django import forms
from .models import PatientInfo, ProviderInfo, PatientMedication

class PatientInfoForm(forms.ModelForm):
    class Meta:
        model = PatientInfo
        fields = ['name', 'age', 'gender', 'is_pregnant', 'is_breastfeeding', 'disease', 'other_health_info']
        widgets = {
            'gender': forms.RadioSelect(choices=[('Male', 'Male'), ('Female', 'Female')]),
            'is_pregnant': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'is_breastfeeding': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
        }

class ProviderInfoForm(forms.ModelForm):
    class Meta:
        model = ProviderInfo
        fields = ['name', 'organization']

class MedicationForm(forms.ModelForm):
    class Meta:
        model = PatientMedication
        fields = ['dosage', 'frequency']
        widgets = {
            'dosage': forms.TextInput(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'frequency': forms.TextInput(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        }

class ProductSearchForm(forms.Form):
    product_name = forms.CharField(max_length=100, required=True, label='제품명', widget=forms.TextInput(attrs={'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}))
