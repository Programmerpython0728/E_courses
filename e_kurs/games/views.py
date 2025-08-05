from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from .models import Game, GameQuestion
from .serializers import GameSerializer, GameQuestionSerializer
from users.core.permissions import IsAdminUserOrReadOnly
from django.shortcuts import get_object_or_404
import random


class GameViewSet(viewsets.ModelViewSet):
    """
    O'yinlar uchun API endpoint.
    Adminlar o'yinlarni yaratishi, tahrirlashi va o'chirishi mumkin, boshqalar faqat o'ynay oladi.
    """
    queryset = Game.objects.filter(is_active=True)
    serializer_class = GameSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def start(self, request, pk=None):
        """
        O'yinni boshlash. O'yinning birinchi savolini qaytaradi.
        """
        game = get_object_or_404(Game, pk=pk, is_active=True)
        questions = game.questions.all()
        if not questions:
            return Response({"error": "Ushbu o'yin uchun savollar mavjud emas."}, status=status.HTTP_404_NOT_FOUND)

        # Tasodifiy savolni tanlash
        first_question = random.choice(questions)
        serializer = GameQuestionSerializer(first_question)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def check_answer(self, request, pk=None):
        """
        Foydalanuvchi javobini tekshirish va ball berish.
        So'rovda `question_id` va `answer` maydonlari bo'lishi kerak.
        """
        user_answer = request.data.get('answer')
        question_id = request.data.get('question_id')

        if not user_answer or not question_id:
            return Response({"error": "Javob va savol ID'si kiritilishi shart."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            question = GameQuestion.objects.get(id=question_id, game__pk=pk)
        except GameQuestion.DoesNotExist:
            return Response({"error": "Savol topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        if user_answer == question.correct_answer:
            # Foydalanuvchiga ball berish
            user = request.user
            user.points += question.game.reward_points
            user.save()
            return Response({"is_correct": True, "message": "Javobingiz to'g'ri! Sizga {} ball berildi.".format(
                question.game.reward_points)}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"is_correct": False, "correct_answer": question.correct_answer, "message": "Javobingiz noto'g'ri."},
                status=status.HTTP_200_OK)


class GameQuestionViewSet(viewsets.ModelViewSet):
    """
    O'yin savollarini boshqarish uchun faqat adminlarga mo'ljallangan API endpoint.
    """
    queryset = GameQuestion.objects.all()
    serializer_class = GameQuestionSerializer
    permission_classes = [IsAdminUser]
