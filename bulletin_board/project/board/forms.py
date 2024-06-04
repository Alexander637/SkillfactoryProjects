from django import forms
from .models import Advertisement, Response
from ckeditor.widgets import CKEditorWidget


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'content', 'category']
        widgets = {
            'content': CKEditorWidget(),
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']


class ResponseFilterForm(forms.Form):
    advertisement = forms.ModelChoiceField(queryset=Advertisement.objects.all(), required=False, label='Advertisement')
