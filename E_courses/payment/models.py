from django.db import models
from django.conf import settings


class Payment(models.Model):
    # Foydalanuvchini, kim to'lov qilayotganini aniqlaymiz.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='payments')

    # To'lov summasi. Max_digits - jami raqamlar soni, decimal_places - verguldan keyingi raqamlar soni.
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Valyuta turi (masalan, USD, UZS).
    currency = models.CharField(max_length=3, default='UZS')

    # To'lovning holati. 'pending' - kutilmoqda, 'completed' - yakunlandi, 'failed' - xato.
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Kutilmoqda'),
            ('completed', 'Yakunlandi'),
            ('failed', 'Xato')
        ],
        default='pending'
    )

    # To'lov haqida qisqacha ma'lumot.
    description = models.TextField(blank=True)

    # To'lov tizimidan olingan noyob tranzaksiya ID si (masalan, Stripe ID).
    transaction_id = models.CharField(max_length=255, blank=True, null=True)

    # To'lov amalga oshirilgan sana va vaqt.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} {self.currency} by {self.user}"

    class Meta:
        verbose_name = "To'lov"
        verbose_name_plural = "To'lovlar"
