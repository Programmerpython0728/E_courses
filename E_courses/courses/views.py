from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from .models import Course, Lesson, UserCourse
from .serializers import CourseListSerializer, CourseDetailSerializer, LessonSerializer, UserCourseSerializer
from users.core.permissions import IsTeacherOrReadOnly

class CourseViewSet(viewsets.ModelViewSet):
    """
    Kurslarni yaratish, ko'rish, tahrirlash va o'chirish uchun API endpoint.
    Admin va o'qituvchilar kurslarni boshqarish huquqiga ega, boshqalar faqat o'qiy oladi.
    """
    queryset = Course.objects.filter(is_active=True)
    permission_classes = [IsTeacherOrReadOnly]

    def get_serializer_class(self):
        """ Har xil so'rovlar uchun turli serializerlarni qaytaradi. """
        if self.action in ['retrieve', 'update', 'partial_update']:
            return CourseDetailSerializer
        return CourseListSerializer

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def my_courses(self, request):
        """
        Avtorizatsiyadan o'tgan foydalanuvchi sotib olgan kurslar ro'yxatini qaytaradi.
        URL: /api/v1/courses/my-courses/
        """
        purchased_courses = UserCourse.objects.filter(user=request.user)
        serializer = UserCourseSerializer(purchased_courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def purchase_course(self, request, pk=None):
        """
        Foydalanuvchi kurs sotib olishi uchun endpoint.
        URL: /api/v1/courses/{id}/purchase_course/
        """
        try:
            course = self.get_object()
        except Course.DoesNotExist:
            return Response({"detail": "Kurs topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        if UserCourse.objects.filter(user=request.user, course=course).exists():
            return Response({"detail": "Siz bu kursni allaqachon sotib olgansiz."}, status=status.HTTP_400_BAD_REQUEST)

        if course.price == 0:
            UserCourse.objects.create(user=request.user, course=course)
            return Response({"message": "Kurs muvaffaqiyatli sotib olindi!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "To'lov amalga oshirilishi kerak."}, status=status.HTTP_200_OK)

class LessonCreateView(generics.CreateAPIView):
    """
    Kursga yangi dars qo'shish uchun endpoint. Faqat o'qituvchilar uchun.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsTeacherOrReadOnly]

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if course.teacher != self.request.user:
            return Response(
                {"detail": "Siz ushbu kursga dars qo'sha olmaysiz."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

