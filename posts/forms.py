from django import forms
from posts.models import Post, postExtraImages
from cloudinary.forms import CloudinaryFileField


class NewPostForm(forms.ModelForm):
    image = CloudinaryFileField(required=True)
    caption = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'input is-medium'}), required=True, max_length=150)

    class Meta:
        model = Post
        fields = ('image', 'caption')


class CarouselPostForm(forms.ModelForm):
    caption = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'input is-medium'}), required=True, max_length=150)

    class Meta:
        model = Post
        fields = ('caption', )
 
 
class ImageForm(forms.ModelForm):
    image = CloudinaryFileField(required=True)    
    class Meta:
        model = postExtraImages
        fields = ('image', )
