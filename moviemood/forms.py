from django import forms

class SearchForm(forms.Form):
    mood = forms.CharField(max_length=50)