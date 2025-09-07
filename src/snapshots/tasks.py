import helpers.bd 
from django.apps import apps

from django_qstash import stashed_task
from celery import shared_task


@stashed_task
def perform_reddit_scrape_task(subreddit_url, num_of_posts: int = 20):
    BrightDataSnapshot = apps.get_model("snapshots", "BrightDataSnapshot")
    data = helpers.bd.perform_scrape_snapshot(subreddit_url, num_of_posts = num_of_posts, raw=True)
    snapshot_id = data.get('snapshot_id')
    instance_id = BrightDataSnapshot.objects.create(
        snapshot_id=snapshot_id,
        dataset_id=helpers.bd.BRIGH_DATA_DATASET_ID,
        status="Unknown",
        url=subreddit_url,
    )
    # start progress checking
    get_snapshot_instance_progress_task.apply_async(args=(instance_id,), countdown=300)
    return snapshot_id


@stashed_task
def get_snapshot_instance_progress_task(instance_id: int) -> bool:
    BrightDataSnapshot = apps.get_model("snapshots", "BrightDataSnapshot")
    instance = BrightDataSnapshot.objects.get(id=instance_id)
    snapshot_id = instance.snapshot_id
    data = helpers.bd.get_snapshot_progress(snapshot_id, raw=True)
    status = data.get('status')
    records = data.get('records') or 0
    instance.records = records
    instance.status = status
    instance.save()
    return status == 'ready'