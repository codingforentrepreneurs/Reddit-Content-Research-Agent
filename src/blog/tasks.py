from celery import shared_task
from django_qstash import stashed_task


@stashed_task
def hello_world(name: str, age: int = None, activity: str = None):
    if age is None:
        print(f"Hello {name}! I see you're {activity}.")
        return
    print(f"Hello {name}! I see you're {activity} at {age} years old.")


@shared_task
def my_blog_task():
    print("hello world")