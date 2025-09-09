from django.db.models.signals import post_save

from .models import RedditCommunity

from . import services as reddit_db_services


def reddit_community_post_save_receiver(sender, instance, created, *args, **kwargs):
    reddit_db_services.handle_reddit_community_scrape_automation(
            instance, 
            created=created, 
            force_scrape=False,
            verbose=True
    )

post_save.connect(reddit_community_post_save_receiver, sender=RedditCommunity)