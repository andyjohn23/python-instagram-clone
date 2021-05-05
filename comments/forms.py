from django import forms
from .models import comments


class commentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'input is-medium'}), required=False)

    class Meta:
        model = comments
        fields = ['body',]
