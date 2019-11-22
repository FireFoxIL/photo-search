from django import forms


class SearchImageForm(forms.Form):
    image = forms.ImageField()
