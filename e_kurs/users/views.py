from rest_framework import viewsets, mixins, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)
from users.core.permissions import IsAdminUserOrReadOnly, IsOwnerOrAdmin

# Parolni tiklash uchun qo'shimcha importlar
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, smart_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """
    Foydalanuvchilarni yaratish, ro'yxatini ko'rish va profilini tahrirlash uchun ViewSet.
    """
    queryset = User.objects.all()

    def get_serializer_class(self):
        """ Har xil so'rovlar uchun turli serializerlarni qaytaradi. """
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserProfileSerializer

    def get_permissions(self):
        """ Har xil amallar uchun turli ruxsatlarni qaytaradi. """
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]  # Adminlar uchun
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]  # O'z profilini tahrirlash
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """ Yangi foydalanuvchini yaratish. """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        """ retrieve, update, partial_update so'rovlari uchun joriy foydalanuvchini qaytaradi. """
        if self.action in ['retrieve', 'update', 'partial_update'] and self.kwargs.get('pk') == 'me':
            return self.request.user
        return super().get_object()


class PasswordResetView(generics.GenericAPIView):
    """ Parolni tiklash so'rovini boshlash uchun API endpoint. """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Foydalanuvchi topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        token_generator = PasswordResetTokenGenerator()
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        # Front-end dasturchisi bilan kelishib olingan URL manzil
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uidb64}/{token}/"

        # Email yuborish
        email_body = render_to_string('password_reset_email.html', {'user': user, 'reset_url': reset_url})
        send_mail(
            subject='Parolni tiklash',
            message=email_body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response({"detail": "Parolni tiklash havolasi elektron pochtangizga yuborildi."},
                        status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    """ Parolni yangilash uchun API endpoint. """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        uid = serializer.validated_data['uid']
        new_password = serializer.validated_data['new_password']

        try:
            uid = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Parolingiz muvaffaqiyatli tiklandi."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Havola yaroqsiz yoki muddati tugagan."}, status=status.HTTP_400_BAD_REQUEST)
