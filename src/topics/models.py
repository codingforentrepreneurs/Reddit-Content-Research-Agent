from django.db import models


from queries.models import Query

from .tasks import topic_to_reddit_community_task
# Create your models here.
# Create your models here.
class Topic(models.Model):
    # user
    name = models.TextField(db_index=True)
    created_by_query = models.ForeignKey(Query, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        topic_to_reddit_community_task.delay(self.name)