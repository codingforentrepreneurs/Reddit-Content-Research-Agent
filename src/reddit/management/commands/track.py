from django.core.management.base import BaseCommand

from reddit.models import RedditCommunity

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Trigger tracking event for Reddit Communities")
        qs = RedditCommunity.objects.trackable()
        for obj in qs:
            name = obj.name
            print(f"Starting {name}")
            obj.save()
