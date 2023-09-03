from django.forms import ModelForm
from .models import Post
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get_or_create(name='common')[0]
        basic_group.user_set.add(user)
        return user

class PostForms(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'choice', 'category', 'postTitle', 'postText']
        widgets = {
            'author': forms.Select(attrs={'class': 'form-control'}),
            'choice': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'postTitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter article title'}),
            'postText': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter article text'})
        }