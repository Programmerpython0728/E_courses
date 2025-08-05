from django.contrib import admin
from .models import AboutPage

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):

    list_display = ('title',)
    fields = ('title', 'content', 'team_members')
