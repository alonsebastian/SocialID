from django import forms

class PersonalPageForm(forms.Form):
    """ Form to reflect the data stored in the PersonalPage model."""
    bio = forms.CharField(max_length=300, required = False, widget=forms.Textarea(attrs={'rows':'2'}))
    location = forms.CharField(max_length=50, required = False, initial = "eg: Richmond, VA, USA.")
    email = forms.CharField(max_length=50, required = False)
    facebook = forms.CharField(max_length=50, required = False)
    twitter = forms.CharField(max_length=50, required = False)
    tumblr = forms.CharField(max_length=80, required = False)
    linkedin = forms.CharField(max_length=80, required = False)
    personal_site = forms.CharField(max_length=50, required = False)
