from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonCreateView

# DefaultRouter avtomatik ravishda CourseViewSet uchun CRUD URL manzillarini yaratadi.
# Ya'ni, GET, POST, PUT, DELETE so'rovlari uchun alohida path yozish shart emas.
router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    # Router orqali CourseViewSet uchun yaratilgan URL manzillari
    path('', include(router.urls)),

    # Dars yaratish uchun maxsus endpoint
    path('lessons/create/', LessonCreateView.as_view(), name='lesson_create'),
]
