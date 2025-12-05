from django import forms
from .models import Quotes


class AddQuoteForm(forms.ModelForm):
    class Meta:
        model = Quotes
        fields = ['title','content','category']


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")