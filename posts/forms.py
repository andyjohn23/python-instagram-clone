from django import forms
from posts.models import Post
from cloudinary.models import CloudinaryField

class NewPostForm(forms.ModelForm):
    photo = forms.CloudinaryField