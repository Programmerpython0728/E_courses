from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class BlogPost(models.Model):
    """
    Blog maqolalari uchun model.
    """
    title = models.CharField(max_length=255, verbose_name=_("Sarlavha"))
    short_description = models.CharField(max_length=500, verbose_name=_("Qisqacha tavsif"))
    content = models.TextField(verbose_name=_("Asosiy matn"))
    image = models.ImageField(upload_to='blog/images/', blank=True, null=True, verbose_name=_("Rasm"))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='blog_posts',
        verbose_name=_("Muallif")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan sana"))
    is_published = models.BooleanField(default=True, verbose_name=_("Nashr qilinganmi"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Blog maqolasi")
        verbose_name_plural = _("Blog maqolalari")

    def __str__(self):
        return self.title
