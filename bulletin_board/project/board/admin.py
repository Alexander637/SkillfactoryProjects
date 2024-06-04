from django.contrib import admin
from .models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'user')
    search_fields = ('title', 'content')
    list_filter = ('category', 'created_at')
    ordering = ('-created_at',)
