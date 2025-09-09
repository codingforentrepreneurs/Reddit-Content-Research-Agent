from django.contrib import admin

# Register your models here.
from .models import Topic


class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_by_query']
    list_filter = ['created_at']

admin.site.register(Topic, TopicAdmin)