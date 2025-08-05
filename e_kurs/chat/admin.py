from django.contrib import admin
from .models import ChatHistory

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    """
    Django admin paneli orqali ChatHistory modelini boshqarish.
    """
    list_display = ('user', 'prompt', 'created_at')
    list_filter = ('user',)
    search_fields = ('user__email', 'prompt', 'response')
    readonly_fields = ('user', 'prompt', 'response', 'created_at')

