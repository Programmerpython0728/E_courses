from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    """
    To'lov modelini seriyalashtirish uchun seriyalashtiruvchi.
    """
    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'currency', 'status', 'description', 'transaction_id', 'created_at']
        read_only_fields = ['user', 'status', 'transaction_id', 'created_at']

class CreateChargeSerializer(serializers.Serializer):
    """
    To'lov yaratish uchun keladigan ma'lumotlarni tekshirish uchun seriyalashtiruvchi.
    """
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3, default='UZS')
    description = serializers.CharField(required=False, allow_blank=True)
    # real loyihalarda token/payment method ID kabi ma'lumotlar ham talab qilinadi.
    # Bu misolda soddalashtirilgan.
