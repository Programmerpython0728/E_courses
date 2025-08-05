from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import BlogPost
from .serializers import BlogPostListSerializer, BlogPostDetailSerializer
from users.core.permissions import IsAdminUserOrReadOnly

class BlogViewSet(viewsets.ModelViewSet):
    """
    Blog maqolalarini boshqarish uchun API endpoint.
    Foydalanuvchilar faqat o'qiy oladi, admin esa to'liq CRUD amallarini bajara oladi.
    """
    queryset = BlogPost.objects.filter(is_published=True)
    permission_classes = [IsAdminUserOrReadOnly]

    def get_serializer_class(self):
        """
        GET so'rovi uchun ListSerializer, boshqa amallar uchun DetailSerializer ishlatiladi.
        """
        if self.action == 'list':
            return BlogPostListSerializer
        return BlogPostDetailSerializer

    def perform_create(self, serializer):
        """
        Maqola yaratilishida muallifni avtomatik ravishda belgilash.
        """
        serializer.save(author=self.request.user)
