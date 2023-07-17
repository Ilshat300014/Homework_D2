from django.forms import ModelForm
from .models import Post
from django import forms

class PostForms(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'choice', 'category', 'postTitle', 'postText']
        widgets = {
            'author': forms.Select(attrs={'class': 'form-control'}),
            'choice': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'postTitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter article title'}),
            'postText': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter article text'})
        }