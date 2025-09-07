from django.db import models

# Create your models here.
class BrightDataSnapshot(models.Model):
    snapshot_id = models.CharField(max_length=120)
    dataset_id = models.CharField(max_length=120)
    status = models.CharField(max_length=120)
    error_msg = models.TextField(null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    # created_at
    # finished_at


    @property
    def is_ready(self) -> bool:
        if self.error_msg:
            return False
        return self.status == "ready"