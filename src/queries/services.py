import ai

from topics.models import Topic


def perform_topic_extraction(query_instance):
    query_text = query_instance.text
    topics_list = ai.extract_topics_agent(query_text)
    # instance = Query.objects.create(text=query_text)
    for topic_item in topics_list:
        topic_obj, created = Topic.objects.update_or_create(
            name=topic_item.get('name'),
            defaults = {
                "slug": topic_item.get('slug')
            }
        )
        if created:
            topic_obj.created_by_query = query_instance
            topic_obj.save()
    return topics_list