from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameViewSet, GameQuestionViewSet

# Router Game va GameQuestion modellari uchun avtomatik URL manzillar yaratadi.
router = DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'questions', GameQuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
