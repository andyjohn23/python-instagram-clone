from django import forms
from posts.models import Post


class NewPostForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    caption = forms.Textarea(widget=forms.Textarea(attrs=('class': 'input is-medium')), required=True)

    class Meta:
        model = Post
        fields = ['image', 'caption']
