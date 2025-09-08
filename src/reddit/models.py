from django.db import models

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
        auto_now=True, 
        null=True, 
        blank=True
    )

    def __str__(self):
        if not self.title:
            return f"{self.url}"
        return f"{self.title}"