from django import forms


class UploadImageForm(forms.Form):
    image = forms.ImageField()


class SearchImageForm(forms.Form):
    image = forms.ImageField()
