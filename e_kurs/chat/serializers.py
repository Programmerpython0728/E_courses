from rest_framework import serializers
from .models import ChatHistory

class ChatHistorySerializer(serializers.ModelSerializer):
    """
    Suhbat tarixini ko'rsatish uchun .
    """
    class Meta:
        model = ChatHistory
        fields = ('id', 'prompt', 'response', 'created_at')
        read_only_fields = ('response', 'created_at')

class ChatPromptSerializer(serializers.Serializer):
    """
    Foydalanuvchining yangi savolini qabul qilish uchun .
    """
    prompt = serializers.CharField(max_length=5000)

