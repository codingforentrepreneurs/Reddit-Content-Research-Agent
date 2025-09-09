from datetime import timedelta
import helpers.bd
from django.db.models.signals import post_save
from django.utils import timezone

from snapshots.tasks import perform_reddit_scrape_task

from .models import RedditCommunity
from . import services


def reddit_community_post_save_receiver(sender, instance, created, *args, **kwargs):
    # print(instance.pk, instance.url)
    services.handle_reddit_community_scraping(instance, created)
    

post_save.connect(reddit_community_post_save_receiver, sender=RedditCommunity)