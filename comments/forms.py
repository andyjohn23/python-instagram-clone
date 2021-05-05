from django import forms
from .models import Comments


class commentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'input is-medium'}), required=False)

    class Meta:
        model = Comments
        fields = ['body']
