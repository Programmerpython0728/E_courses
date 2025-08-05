from rest_framework import serializers
from .models import Game, GameQuestion

class GameQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameQuestion
        fields = ('id', 'question_text', 'options', 'correct_answer')
        extra_kwargs = {
            'correct_answer': {'write_only': True}
        }

class GameSerializer(serializers.ModelSerializer):
    questions = GameQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ('id', 'name', 'game_type', 'reward_points', 'questions')
