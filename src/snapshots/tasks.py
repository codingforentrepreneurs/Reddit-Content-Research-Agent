from datetime import timedelta
from django.utils.html import CountsDict
import helpers.bd 
from django.apps import apps
from django.utils import timezone

from django_qstash import stashed_task
from celery import shared_task

MAX_PROGRESS_INTERATION_COUNT = 10

@stashed_task
def perform_reddit_scrape_task(
        subreddit_url, 
        num_of_posts: int = 20, 
        progress_countdown: int=300,
        sort_by_time: str = "This Week"):
    BrightDataSnapshot = apps.get_model("snapshots", "BrightDataSnapshot")
    data = helpers.bd.perform_scrape_snapshot(
            subreddit_url, 
            num_of_posts = num_of_posts, 
            raw=True,
            sort_by_time=sort_by_time
    )
    snapshot_id = data.get('snapshot_id')
    instance = BrightDataSnapshot.objects.create(
        snapshot_id=snapshot_id,
        dataset_id=helpers.bd.BRIGHT_DATA_DATASET_ID,
        url=subreddit_url,
    )
    # start progress checking
    get_snapshot_instance_progress_task.apply_async(args=(instance.id,), countdown=progress_countdown)
    return snapshot_id


@stashed_task
def get_snapshot_instance_progress_task(instance_id: int) -> bool:
    BrightDataSnapshot = apps.get_model("snapshots", "BrightDataSnapshot")
    instance = BrightDataSnapshot.objects.get(id=instance_id)
    progress_check_count = instance.progress_check_count
    new_progress_check_count = progress_check_count + 1
    snapshot_id = instance.snapshot_id
    data = helpers.bd.get_snapshot_progress(snapshot_id, raw=True)
    status = data.get('status')
    records = data.get('records') or 0
    instance.records = records
    instance.status = status
    instance.progress_check_count = new_progress_check_count
    instance.save()
    instance.refresh_from_db()
    progress_complete = instance.progress_complete
    if not progress_complete and new_progress_check_count < MAX_PROGRESS_INTERATION_COUNT:
        print("Recheck how our snapshot is doing")
        delay_delta = 30 * new_progress_check_count
        get_snapshot_instance_progress_task.apply_async(
                args=(instance_id,), 
            countdown=delay_delta
        )
        return 
    return status == 'ready'




@stashed_task
def download_snapshot_to_reddit_post(instance_id:int = None):
    from reddit import services as reddit_db_services
    BrightDataSnapshot = apps.get_model("snapshots", "BrightDataSnapshot")
    try:
        instance = BrightDataSnapshot.objects.get(id=instance_id)
    except:
        return 
    try:
        reddit_results = helpers.bd.download_snapshot(instance.snapshot_id)
    except:
        return
    reddit_db_services.handle_reddit_thread_results(reddit_results)


@stashed_task
def snapshots_download_sync(download_all_available=True):
    BrightDataSnapshot = apps.get_model("snapshots", "BrightDataSnapshot")
    now = timezone.now()
    last_week = now - timedelta(days=8)
    filters = {
        "status": "ready",
        "records__gt": 0,
    }
    if not download_all_available:
        filters[ "last_result_sync__lte"] = last_week
    qs = BrightDataSnapshot.objects.filter(
            **filters
        ).order_by('-id')
    for idx, instance in enumerate(qs):
        delay_delta = 30 * idx
        download_snapshot_to_reddit_post.apply_async(kwargs = {
            "instance_id": instance.id,
        }, countdown=delay_delta)
    qs.update(last_result_sync=timezone.now())