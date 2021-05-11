from django import forms
from posts.models import Post, postExtraImages
from cloudinary.forms import CloudinaryFileField
from django.forms import ClearableFileInput


class NewPostForm(forms.ModelForm):
    content = CloudinaryFileField(widget=forms.ClearableFileInput(
        attrs={'multiple':True}), required=True)
    caption = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'input is-medium'}), required=True, max_length=150)

    class Meta:
        model = Post
        fields = ('content', 'caption')


class CarouselPostForm(forms.ModelForm):
    content = CloudinaryFileField(required=True)
    caption = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'input is-medium'}), required=True, max_length=150)

    class Meta:
        model = Post
        fields = ('content', 'caption')


class ImageForm(forms.ModelForm):
    image = CloudinaryFileField(required=True)

    class Meta:
        model = postExtraImages
        fields = ('image', )
