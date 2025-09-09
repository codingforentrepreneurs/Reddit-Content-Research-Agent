from functools import lru_cache
from datetime import timedelta
import helpers.bd
from django.utils import timezone

from snapshots.tasks import perform_reddit_scrape_task

from .models import RedditPost, RedditCommunity

@lru_cache
def get_valid_reddit_post_fields():
    model_field_names = [field.name for field in RedditPost._meta.get_fields()]
    skip_fields = ['id', 'post_id', 'url',]
    valid_fields = [x for x in model_field_names if x not in skip_fields]
    return valid_fields


def handle_reddit_thread_results(reddit_results:list = []):
    valid_fields = get_valid_reddit_post_fields()
    ids = []
    for thread in reddit_results:
        post_id = thread.get("post_id")
        url = thread.get("url")
        if not all([url, post_id]):
            continue
        update_data = {k:v for k, v in thread.items() if k in valid_fields}
        instance, _ = RedditPost.objects.update_or_create(
            post_id=post_id,
            url=url,
            defaults=update_data
        )
        ids.append(instance.id)
    return ids




def handle_reddit_community_scrape_automation(instance, created=False, force_scrape=False, verbose=False):
    # print(instance.pk, instance.url)
    instance.refresh_from_db()
    url = instance.url
    active = instance.active 
    if not active and not force_scrape:
        return
    now = timezone.now()
    last_scrape_event = instance.last_scrape_event
    last_event_delta = None
    min_last_event_delta = timedelta(minutes=5)
    if last_scrape_event is not None:
        last_event_delta = now - last_scrape_event
        scrape_ready = last_event_delta > min_last_event_delta
    else:
        scrape_ready = True
    if force_scrape:
        scrape_ready = True
    if verbose:
        print("Ready to scrape",scrape_ready, instance.url)
        print("Was jsut created", created)
    qs = RedditCommunity.objects.filter(pk=instance.pk)
    qs.update(last_scrape_event = timezone.now())
    if scrape_ready and not created:
        if verbose:
            print("Trigger reddit community post scrape update")
        perform_reddit_scrape_task.delay(
            url, 
            num_of_posts = 5, 
            progress_countdown=300,
            sort_by_time = "This Week"
        )
    if created:
        if verbose:
            print("First pass reddit community run")
        for sort_by in helpers.bd.BRIGHT_DATA_SCRAPE_SORT_OPTIONS:
            perform_reddit_scrape_task.delay(
                url, 
                num_of_posts = 5, 
                progress_countdown=300,
                sort_by_time=sort_by
            )
    if verbose:
        print("---done---\n")