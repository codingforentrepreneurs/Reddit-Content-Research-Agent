from django.db import models

# Create your models here.
class Query(models.Model):
    # user
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text}"[:30]