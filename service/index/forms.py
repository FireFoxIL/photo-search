from django import forms


class UploadImageForm(forms.Form):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class SearchImageForm(forms.Form):
    image = forms.ImageField()
