from django.contrib import admin

# Register your models here.
from .models import RedditPost

admin.site.register(RedditPost)