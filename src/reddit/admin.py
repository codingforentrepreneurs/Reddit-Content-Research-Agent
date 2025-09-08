from django.contrib import admin

# Register your models here.
from .models import RedditCommunity, RedditPost

class RedditCommunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'subreddit_slug', 'member_count']

admin.site.register(RedditCommunity, RedditCommunityAdmin)

class RedditPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'community_name']
    list_filter = ['community_name']

admin.site.register(RedditPost, RedditPostAdmin)