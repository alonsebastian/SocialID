from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'pattern': '[0-9a-zA-Z]{4,8}'}))
