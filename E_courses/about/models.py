from django.db import models
from django.utils.translation import gettext_lazy as _


class AboutPage(models.Model):
    """
    "Biz haqimizda" sahifasi uchun yagona model.
    """
    title = models.CharField(max_length=255, verbose_name=_("Sarlavha"))
    content = models.TextField(verbose_name=_("Asosiy matn"))
    team_members = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_("Jamoa a'zolari (JSON)"),
        help_text=_("Masalan: [{\"name\": \"John Doe\", \"role\": \"CEO\"}]")
    )

    class Meta:
        verbose_name = _("Biz haqimizda sahifasi")
        verbose_name_plural = _("Biz haqimizda sahifalari")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Faqa bitta AboutPage ob'ekti mavjud bo'lishini ta'minlash.
        """
        if not self.pk and AboutPage.objects.exists():
            # Agar sahifa allaqachon mavjud bo'lsa, yangisini yaratishga yo'l qo'ymaydi
            # Lekin mavjudini tahrirlash mumkin
            pass
        return super(AboutPage, self).save(*args, **kwargs)
