from django.db.models.signals import post_save

from .models import Query

from . import services as query_db_services


def query_instance_post_save_receiver(sender, instance, created, *args, **kwargs):
    query_db_services.perform_topic_extraction(instance)

post_save.connect(query_instance_post_save_receiver, sender=Query)