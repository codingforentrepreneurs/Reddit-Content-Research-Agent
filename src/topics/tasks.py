from django_qstash import stashed_task

from reddit import services as reddit_db_services

@stashed_task
def topic_to_reddit_community_task(task_name):
    reddit_db_services.handle_topic_to_reddit_community(task_name)