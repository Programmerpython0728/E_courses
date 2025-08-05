from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class Game(models.Model):
    """
    O'yinlar uchun asosiy model.
    """
    GAME_TYPES = [
        ('Test', 'Test'),
        ('Tarjima', 'Tarjima'),
        ('To_g_ri_variant', 'To\'g\'ri variantni tanlash'),
    ]
    name = models.CharField(max_length=255, verbose_name=_("O'yin nomi"))
    game_type = models.CharField(max_length=20, choices=GAME_TYPES, verbose_name=_("O'yin turi"))
    reward_points = models.PositiveIntegerField(default=10, verbose_name=_("Mukofot ballari"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faollik"))

    class Meta:
        verbose_name = _("O'yin")
        verbose_name_plural = _("O'yinlar")

    def __str__(self):
        return self.name

class GameQuestion(models.Model):
    """
    O'yin savollari uchun model.
    """
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name=_("Qaysi o'yinga tegishli")
    )
    question_text = models.TextField(verbose_name=_("Savol"))
    correct_answer = models.CharField(max_length=500, verbose_name=_("To'g'ri javob"))
    options = models.JSONField(verbose_name=_("Variantlar (JSON list)"), help_text=_("Masalan: [\"Variant1\", \"Variant2\", \"Variant3\"]"))

    class Meta:
        verbose_name = _("O'yin savoli")
        verbose_name_plural = _("O'yin savollari")

    def __str__(self):
        return f"{self.game.name} - {self.question_text[:50]}..."
