from functools import lru_cache

from .models import RedditPost

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