from rest_framework import generics
from rest_framework.response import Response
from .models import AboutPage
from .serializers import AboutPageSerializer
from django.shortcuts import get_object_or_404
from users.core.permissions import IsAdminUserOrReadOnly

class AboutPageView(generics.RetrieveUpdateAPIView):
    """
    "Biz haqimizda" sahifasini ko'rish va tahrirlash uchun API endpoint.
    Adminlar tahrirlashi mumkin, boshqalar faqat o'qiy oladi.
    """
    queryset = AboutPage.objects.all()
    serializer_class = AboutPageSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_object(self):
        """
        Faqa bitta AboutPage ob'ekti mavjud bo'lishini ta'minlash
        va uni qaytarish.
        """
        if not self.queryset.exists():
            return AboutPage.objects.create(title="Biz Haqimizda", content="Bu yerda platforma haqida ma'lumot bo'ladi.")
        return get_object_or_404(self.queryset, pk=self.queryset.first().pk)
