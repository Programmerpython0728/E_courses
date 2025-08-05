from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class ChatHistory(models.Model):
    """
    Foydalanuvchi va ChatGPT o'rtasidagi suhbat tarixini saqlash uchun model.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_history',
        verbose_name=_("Foydalanuvchi")
    )
    prompt = models.TextField(verbose_name=_("Foydalanuvchi savoli (Prompt)"))
    response = models.TextField(verbose_name=_("AI javobi (Response)"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan sana"))

    class Meta:
        verbose_name = _("Suhbat tarixi")
        verbose_name_plural = _("Suhbatlar tarixi")
        ordering = ['-created_at']

    def __str__(self):
        return f"Suhbat {self.user.email} bilan {self.created_at}"
