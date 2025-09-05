from celery import shared_task


@shared_task
def my_blog_task():
    print("hello world")