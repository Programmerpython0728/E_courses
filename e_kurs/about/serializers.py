from rest_framework import serializers
from .models import AboutPage

class AboutPageSerializer(serializers.ModelSerializer):
    """
    AboutPage modeli uchun seriyalashtiruvchi.
    """
    class Meta:
        model = AboutPage
        fields = '__all__'
