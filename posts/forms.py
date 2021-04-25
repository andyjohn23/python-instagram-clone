from django import forms
from posts.models import Post
from cloudinary.forms import CloudinaryFileField


class NewPostForm(forms.ModelForm):
    image = CloudinaryFileField(required=True)
    caption = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'input is-medium'}), required=True)

    class Meta:
        model = Post
        fields = ('image', 'caption')
