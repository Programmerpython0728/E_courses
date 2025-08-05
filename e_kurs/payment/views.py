from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from .serializers import CreateChargeSerializer, PaymentSerializer


# Haqiqiy loyihada payment gateway'ga bog'lanuvchi servislarni shu yerda yozasiz
# Hozircha faqat simulyatsiya qilamiz
def mock_process_payment(amount, currency):
    """
    To'lovni qayta ishlashni simulyatsiya qiladi.
    Haqiqiy loyihada bu yerda Stripe yoki boshqa payment gateway API chaqiriladi.
    """
    # Ma'lumotlaringizni tekshiring va to'lovni qayta ishlashni boshlang
    print(f"To'lov simulyatsiyasi: {amount} {currency}")

    # Simulyatsiya natijasi: muvaffaqiyatli to'lov.
    is_successful = True
    transaction_id = "mock_tx_id_" + str(hash(amount))  # Noyob ID

    if is_successful:
        return 'completed', transaction_id
    else:
        return 'failed', None


class CreateChargeView(generics.CreateAPIView):
    """
    Yangi to'lov yaratish uchun API View.
    Faqat autentifikatsiya qilingan foydalanuvchilar kirishi mumkin.
    """
    serializer_class = CreateChargeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Kelgan ma'lumotlarni tekshirish
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        currency = serializer.validated_data['currency']
        description = serializer.validated_data.get('description', '')

        # To'lovni simulyatsiya qilish
        payment_status, transaction_id = mock_process_payment(amount, currency)

        if payment_status == 'completed':
            # Yangi to'lov ob'ektini yaratish va saqlash
            payment = Payment.objects.create(
                user=request.user,
                amount=amount,
                currency=currency,
                description=description,
                status=payment_status,
                transaction_id=transaction_id
            )

            response_serializer = PaymentSerializer(payment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "To'lovni amalga oshirib bo'lmadi."},
                status=status.HTTP_400_BAD_REQUEST
            )
