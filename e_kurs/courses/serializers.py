from rest_framework import serializers
from .models import Course, Lesson, UserCourse
from users.serializers import UserProfileSerializer

class LessonSerializer(serializers.ModelSerializer):
    """
    Dars modelini seriyalashtirish uchun.
    """
    class Meta:
        model = Lesson
        # Barcha maydonlar kiritilgan, lekin kerak bo'lsa cheklash mumkin
        fields = '__all__'

class CourseListSerializer(serializers.ModelSerializer):
    """
    Kurslar ro'yxatini ko'rsatish uchun seriyalashtiruvchi.
    Ro'yxatda faqat asosiy ma'lumotlar ko'rsatiladi.
    """
    teacher = UserProfileSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'price', 'level', 'teacher')

class CourseDetailSerializer(serializers.ModelSerializer):
    """
    Kursning batafsil ma'lumotlarini ko'rsatish uchun seriyalashtiruvchi.
    Ushbu seriyalashtiruvchi Darslar ro'yxatini ham o'z ichiga oladi.
    """
    lessons = LessonSerializer(many=True, read_only=True)
    teacher = UserProfileSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'price', 'level', 'teacher', 'is_active', 'lessons')

class UserCourseSerializer(serializers.ModelSerializer):
    """
    Foydalanuvchi sotib olgan kurslarni ko'rsatish uchun seriyalashtiruvchi.
    """
    course = CourseListSerializer(read_only=True)

    class Meta:
        model = UserCourse
        fields = ('id', 'course', 'purchase_date')

