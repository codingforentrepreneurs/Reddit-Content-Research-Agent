from django.contrib import admin

# Register your models here.
from .models import RedditCommunity, RedditPost

class RedditCommunityAdmin(admin.ModelAdmin):
    list_display = ['subreddit_slug', 'member_count', 'trackable', 'active']
    search_fields = ['name', 'subreddit_slug', 'url']
    list_filter = ['trackable', 'active']
    list_editable = ['trackable', 'active']

admin.site.register(RedditCommunity, RedditCommunityAdmin)

class RedditPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'community_name']
    list_filter = ['community_name']

admin.site.register(RedditPost, RedditPostAdmin)