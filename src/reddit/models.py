from django.db import models


class RedditCommunityManager(models.Manager):
    def trackable(self):
        return self.get_queryset().filter(active=True, trackable=True)

class RedditCommunity(models.Model):
    url = models.URLField(db_index=True, help_text="The complete url of the reddit community")
    name = models.TextField(null=True, blank=True, help_text="Formatted name for Reddit")
    subreddit_slug= models.CharField(max_length=400, null=True, blank=True, help_text="The slug of the subbreddit such as r/python or r/web or r/trending")
    member_count = models.IntegerField(blank=True, null=True, help_text="Current member count, if available.")
    active = models.BooleanField(default=True, help_text="Is this searchable?")
    trackable = models.BooleanField(default=False, help_text="Is this currently being tracked")
    last_scrape_event = models.DateTimeField(
        auto_now_add=False, 
        auto_now=False, 
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RedditCommunityManager()

    # def save(self, *args, **kwargs):
    #     is_valid_reddit_url = ai.check_url()
    #     self.active = False

# Create your models here.
class RedditPost(models.Model):
    # id
    post_id = models.CharField(max_length=120, db_index=True)
    url = models.URLField(db_index=True)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    comments = models.JSONField(blank=True, null=True)
    related_posts = models.JSONField(blank=True, null=True)
    community_name = models.TextField(null=True, blank=True)
    num_upvotes = models.IntegerField(blank=True, null=True)
    num_comments = models.IntegerField(blank=True, null=True)
    date_posted = models.DateTimeField(
        auto_now_add=False, 
        auto_now=False, 
        null=True, 
        blank=True
    )

    def __str__(self):
        if not self.title:
            return f"{self.url}"
        return f"{self.title}"