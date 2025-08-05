from django.contrib import admin
from .models import Game, GameQuestion

class GameQuestionInline(admin.TabularInline):
    """
    Game modelini tahrirlash sahifasida GameQuestion ob'ektlarini ko'rsatish.
    """
    model = GameQuestion
    extra = 1  # Yangi savollar uchun nechta bo'sh maydon ko'rsatilishi

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """
    Django admin paneli orqali Game modelini boshqarish.
    """
    list_display = ('name', 'game_type', 'reward_points', 'is_active')
    list_filter = ('game_type', 'is_active')
    search_fields = ('name',)
    inlines = [GameQuestionInline]

@admin.register(GameQuestion)
class GameQuestionAdmin(admin.ModelAdmin):
    """
    Django admin paneli orqali GameQuestion modelini boshqarish.
    """
    list_display = ('question_text', 'game', 'correct_answer')
    search_fields = ('question_text',)
    list_filter = ('game',)
