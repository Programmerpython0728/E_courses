from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """
    Django admin paneli orqali BlogPost modelini boshqarish.
    """
    list_display = ('title', 'author', 'created_at', 'is_published')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)

