from rest_framework import serializers
from .models import BlogPost
from users.serializers import UserProfileSerializer

class BlogPostListSerializer(serializers.ModelSerializer):
    """
    Blog maqolalari ro'yxatini ko'rsatish uchun seriyalashtiruvchi.
    """
    author = UserProfileSerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'short_description', 'image', 'author', 'created_at')

class BlogPostDetailSerializer(serializers.ModelSerializer):
    """
    Blog maqolasining batafsil ma'lumotlarini ko'rsatish uchun seriyalashtiruvchi.
    """
    author = UserProfileSerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = '__all__'

