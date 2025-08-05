from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Course(models.Model):
    """
    Kurslar uchun asosiy model.
    """
    COURSE_LEVELS = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('IELTS-ready', 'IELTS-ready'),
    ]

    title = models.CharField(max_length=255, verbose_name=_("Kurs nomi"))
    description = models.TextField(verbose_name=_("Tavsifi"))
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Narxi"))

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'Teacher'},
        related_name='courses',
        verbose_name=_("Muallif (o'qituvchi)")
    )
    level = models.CharField(max_length=20, choices=COURSE_LEVELS, default='Beginner', verbose_name=_("Bosqich"))
    is_active = models.BooleanField(default=True, verbose_name=_("Faollik"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan sana"))

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name=_("Qaysi kursga tegishli")
    )
    title = models.CharField(max_length=255, verbose_name=_("Dars nomi"))
    content = models.TextField(verbose_name=_("Dars mazmuni"))
    video_file = models.FileField(
        upload_to='lessons/videos/',
        blank=True, null=True,
        verbose_name=_("Video fayl (yuklangan)")
    )
    video_link = models.URLField(
        max_length=200,
        blank=True, null=True,
        verbose_name=_("Video link (YouTube yoki boshqa)")
    )
    files = models.FileField(
        upload_to='lessons/files/',
        blank=True, null=True,
        verbose_name=_("Qo'shimcha fayllar (PDF)")
    )
    order_number = models.PositiveIntegerField(verbose_name=_("Tartib raqami"))

    class Meta:
        ordering = ['order_number']
        unique_together = ('course', 'order_number')
        verbose_name = _("Dars")
        verbose_name_plural = _("Darslar")

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class UserCourse(models.Model):
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='purchased_courses',
        verbose_name=_("Foydalanuvchi")
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='students',
        verbose_name=_("Kurs")
    )
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Xarid sanasi"))

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = _("Sotib olingan kurs")
        verbose_name_plural = _("Sotib olingan kurslar")

    def __str__(self):
        return f"{self.user.email} - {self.course.title}"
