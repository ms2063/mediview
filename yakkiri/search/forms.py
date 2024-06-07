from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Search for products', max_length=255)
