from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ChatHistory
from .serializers import ChatHistorySerializer, ChatPromptSerializer
import openai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class ChatHistoryView(generics.ListAPIView):

    serializer_class = ChatHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatHistory.objects.filter(user=self.request.user)


class ChatView(generics.CreateAPIView):

    serializer_class = ChatPromptSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_prompt = serializer.validated_data['prompt']

        openai.api_key = settings.OPENAI_API_KEY

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "Siz ingliz tilini o'rganish va IELTSga tayyorlanish bo'yicha yordamchi botisiz. Boshqa savollarga javob bermang."},
                    {"role": "user", "content": user_prompt}
                ]
            )
            chatgpt_response = response.choices[0].message['content']


            ChatHistory.objects.create(
                user=request.user,
                prompt=user_prompt,
                response=chatgpt_response
            )

            return Response({"response": chatgpt_response}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"ChatGPT API bilan bog'lanishda xato: {e}")
            return Response({"error": "Hozircha suhbatlashish imkonsiz. Keyinroq urinib ko'ring."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

