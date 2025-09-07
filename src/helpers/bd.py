
import requests

from django.apps import apps
from django.conf import settings


def get_crawl_headers():
    return {
	"Authorization": f"Bearer {settings.BRIGHT_DATA_REDDIT_SCRAPER_API_KEY}",
	"Content-Type": "application/json",
}


def perform_scrape_snapshot(subreddit_url, num_of_posts: int = 20):
    BrightDataSnapshot = apps.get_model("snapshots", "BrightDataSnapshot")
    url = "https://api.brightdata.com/datasets/v3/trigger"
    dataset_id =  "gd_lvz8ah06191smkebj4"
    headers = get_crawl_headers()
    params = {
    	"dataset_id": dataset_id,
    	"include_errors": "true",
    	"type": "discover_new",
    	"discover_by": "subreddit_url",
    	"limit_per_input": "100",
    }
    data = [
    	{"url": f"{subreddit_url}","sort_by":"Top","sort_by_time":"Today","num_of_posts":num_of_posts},
    ]
    
    response = requests.post(url, headers=headers, params=params, json=data)
    response.raise_for_status()
    data = response.json()
    snapshot_id = data.get('snapshot_id')
    BrightDataSnapshot.objects.create(
        snapshot_id=snapshot_id,
        dataset_id=dataset_id,
        status="Unknown",
        url=subreddit_url,
    )
    return snapshot_id


def get_snapshot_progress(snapshot_id: str) -> bool:
    BrightDataSnapshot = apps.get_model("snapshots", "BrightDataSnapshot")
    url = f"https://api.brightdata.com/datasets/v3/progress/{snapshot_id}"
    headers = get_crawl_headers()
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    snapshot_id = data.get('snapshot_id')
    dataset_id= data.get('dataset_id')
    status =  data.get('status')
    BrightDataSnapshot.objects.update_or_create(
        snapshot_id=snapshot_id,
        dataset_id=dataset_id,
        defaults = {
            "status": status
        }
    )
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
        dataset_id =  "gd_lvz8ah06191smkebj4"
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