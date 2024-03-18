from django import forms
from .models import Author, Post, Category


class PostForm(forms.ModelForm):
    title = forms.CharField(label='Title')
    text = forms.CharField(label='text', widget=forms.Textarea)
    author = forms.ModelChoiceField(
        label='Author',
        queryset=Author.objects.all(),
    )
    category = forms.ModelChoiceField(
        label='Post Category',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'category']




