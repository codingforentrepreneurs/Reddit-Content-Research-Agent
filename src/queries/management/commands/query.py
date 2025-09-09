from django.core.management.base import BaseCommand

from queries.models import Query

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("👋 Hi! What topics would you like me to research for you?")
        user_query  = input("> ").strip()
        if not user_query:
            print("I need something to proceed")
            return 
        Query.objects.create(text=user_query)
        print("Great, we'll review topics that relate and update the database.")
