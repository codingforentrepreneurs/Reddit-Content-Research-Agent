from django_qstash import shared_task
from django.apps import apps



@shared_task
def trigger_trackable_reddit_communities_task():
    RedditCommunity = apps.get_model("reddit", "RedditCommunity")
    qs = RedditCommunity.objects.trackable()
    for obj in qs:
        obj.save()