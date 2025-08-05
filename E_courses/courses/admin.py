from django.contrib import admin
from .models import Course, Lesson, UserCourse

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Django admin paneli orqali Course modelini boshqarish.
    """
    list_display = ('title', 'teacher', 'price', 'level', 'is_active', 'created_at')
    list_filter = ('is_active', 'level', 'teacher')
    search_fields = ('title', 'description', 'teacher__first_name', 'teacher__last_name')
    list_editable = ('is_active',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Django admin paneli orqali Lesson modelini boshqarish.
    """
    list_display = ('title', 'course', 'order_number')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    ordering = ('course', 'order_number')

@admin.register(UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    """
    Django admin paneli orqali UserCourse modelini boshqarish.
    """
    list_display = ('user', 'course', 'purchase_date')
    list_filter = ('purchase_date',)
    search_fields = ('user__email', 'course__title')
    readonly_fields = ('purchase_date',)
