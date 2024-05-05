from django import forms
from .models import Author, Post, Category


class PostForm(forms.ModelForm):
    title = forms.CharField(label='Title')
    text = forms.CharField(label='text', widget=forms.Textarea)
    author = forms.ModelChoiceField(
        label='Author',
        queryset=Author.objects.all(),
    )
    category = forms.ModelMultipleChoiceField(
        label='Post Category',
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            initial_categories = self.instance.postCategory.all()
            self.initial['category'] = list(initial_categories)






