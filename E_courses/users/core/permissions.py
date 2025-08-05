from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminUser(BasePermission):
    """
    Faqat admin roliga ega foydalanuvchilarga ruxsat beradi.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'Admin'


class IsAdminUserOrReadOnly(BasePermission):
    """
    Adminlarga yozish (yaratish, tahrirlash) va o'chirishga, boshqalarga faqat
    o'qishga ruxsat beradi.
    """

    def has_permission(self, request, view):
        # GET, HEAD, OPTIONS so'rovlari uchun barcha foydalanuvchilarga ruxsat berish
        if request.method in SAFE_METHODS:
            return True

        # Boshqa so'rovlar (POST, PUT, DELETE) uchun faqat adminlarga ruxsat berish
        return request.user and request.user.is_authenticated and request.user.role == 'Admin'


class IsTeacherOrReadOnly(BasePermission):
    """
    O'qituvchilarga yozish va o'chirishga, boshqalarga faqat
    o'qishga ruxsat beradi.
    """

    def has_permission(self, request, view):
        # GET, HEAD, OPTIONS so'rovlari uchun barcha foydalanuvchilarga ruxsat berish
        if request.method in SAFE_METHODS:
            return True

        # Boshqa so'rovlar uchun faqat o'qituvchilarga ruxsat berish
        return request.user and request.user.is_authenticated and request.user.role == 'Teacher'


class IsOwnerOrAdmin(BasePermission):
    """
    Faoliyat ob'ektining egasi yoki admin bo'lganlarga ruxsat beradi.
    """

    def has_object_permission(self, request, view, obj):
        # Adminlarga barcha amallar uchun ruxsat berish
        if request.user.role == 'Admin':
            return True

        # Ob'ektning egasi bo'lsa ruxsat berish
        return obj.user == request.user

