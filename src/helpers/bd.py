
import requests

from django.apps import apps
from django.conf import settings

from . import defaults

BRIGHT_DATA_DATASET_ID="gd_lvz8ah06191smkebj4"


def get_crawl_headers():
    return {
	"Authorization": f"Bearer {settings.BRIGHT_DATA_REDDIT_SCRAPER_API_KEY}",
	"Content-Type": "application/json",
}


def perform_scrape_snapshot(subreddit_url, num_of_posts: int = 20, raw=False, use_webhook=True):
    # BrightDataSnapshot = apps.get_model("snapshots", "BrightDataSnapshot")
    url = "https://api.brightdata.com/datasets/v3/trigger"
    dataset_id =  BRIGHT_DATA_DATASET_ID
    headers = get_crawl_headers()
    params = {
    	"dataset_id": dataset_id,
    	"include_errors": "true",
    	"type": "discover_new",
    	"discover_by": "subreddit_url",
    	"limit_per_input": "100",
    }
    if use_webhook:
        auth_key = settings.BRIGHT_DATA_WEBHOOK_HANDLER_SECRET_KEY
        webhook_params = {
            "auth_header": f"Basic {auth_key}",
            "notify": "https://hungrypy.com/webhooks/bd/scrape/",
            "format": "json",
            "uncompressed_webhook": "true",
            "include_errors": "true",
        }
        params.update(webhook_params)

    fields = defaults.BRIGHT_DATA_REDDIT_FIELDS
    ignore_fields = ["comments", "related_posts"]
    
    data = {
        "input": [
            {"url": f"{subreddit_url}", 
            "sort_by":"Top","sort_by_time":"Today","num_of_posts":num_of_posts},
        ],
        "custom_output_fields": [x for x in fields if not x in ignore_fields],
    }
    
    response = requests.post(url, headers=headers, params=params, json=data)
    response.raise_for_status()
    response_data = response.json()
    if raw:
        return response_data
    return response_data.get("snapshot_id")


def get_snapshot_progress(snapshot_id: str, raw=False) -> bool:
    url = f"https://api.brightdata.com/datasets/v3/progress/{snapshot_id}"
    headers = get_crawl_headers()
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    if raw:
        return data
    status = data.get('status')
    return status == 'ready'


def download_snapshot(snapshot_id: str) -> dict:
    BrightDataSnapshot = apps.get_model("snapshots", "BrightDataSnapshot")
    url = f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}"
    headers = get_crawl_headers()
    params = {
        "format": "json"
    }
    response = requests.get(url, headers=headers, params=params)
    msg = response.text
    if response.status_code not in range(200, 299):
        dataset_id =  BRIGHT_DATA_DATASET_ID
        qs = BrightDataSnapshot.objects.filter(
            dataset_id=dataset_id,
            snapshot_id=snapshot_id
            
        )
        qs.update(error_msg=msg)
        return {}
    if f'{msg}'.lower() == "snapshot is empty":
        return {}
    data = response.json()
    return data