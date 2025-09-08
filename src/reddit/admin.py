from django.contrib import admin

# Register your models here.
from .models import RedditPost

class RedditPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'community_name']
    list_filter = ['community_name']

admin.site.register(RedditPost, RedditPostAdmin)