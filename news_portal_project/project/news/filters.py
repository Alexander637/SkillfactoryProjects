from django_filters import FilterSet, DateTimeFilter, CharFilter
from django.forms import DateTimeInput
from .models import Post


class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        label='Title',
        lookup_expr='icontains'
    )
    dateCreation = DateTimeFilter(
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Post
        fields = {
            'categoryType': ['exact'],
        }
