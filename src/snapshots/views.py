import json
import helpers.bd
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from reddit import services as reddit_db_services

from .models import BrightDataSnapshot
from .tasks import get_snapshot_instance_progress_task

BRIGHT_DATA_WEBHOOK_HANDLER_SECRET_KEY = settings.BRIGHT_DATA_WEBHOOK_HANDLER_SECRET_KEY

@csrf_exempt
def snapshot_webhook_handler(request):
    # webhook -> POST request
    # django <> POST request without csrf tokens
    if request.method != "POST":
        return HttpResponse("OK")
    
    
    auth = request.headers.get("Authorization")
    if auth.startswith("Basic "):
        token = auth.split(" ")[1]
        if token == f"{BRIGHT_DATA_WEBHOOK_HANDLER_SECRET_KEY}":
            data = {}
            try:
                data = json.loads(request.body.decode('utf-8'))
            except:
                pass
            snapshot_id = data.get("snapshot_id")
            if snapshot_id:
                qs = BrightDataSnapshot.objects.filter(
                    snapshot_id=snapshot_id,
                    dataset_id=helpers.bd.BRIGHT_DATA_DATASET_ID,
                )
                if not qs.exists():
                    instance = BrightDataSnapshot.objects.create(
                        snapshot_id=snapshot_id,
                        dataset_id=helpers.bd.BRIGHT_DATA_DATASET_ID,
                    )
                    get_snapshot_instance_progress_task(instance.id)
                else:
                    instance_ids = qs.values_list("id", flat=True) 
                    for instance_id in instance_ids:
                        get_snapshot_instance_progress_task(instance_id)

    return HttpResponse("OK")



@csrf_exempt
def reddit_post_webhook_handler(request):
    if request.method != "POST":
        return HttpResponse("OK")
    auth = request.headers.get("Authorization")
    if auth.startswith("Basic "):
        token = auth.split(" ")[1]
        if token == f"{BRIGHT_DATA_WEBHOOK_HANDLER_SECRET_KEY}":
            data = []
            try:
                data = json.loads(request.body.decode('utf-8'))
            except:
                pass
            pass
            reddit_db_services.handle_reddit_thread_results(reddit_results=data)
    return HttpResponse("OK")