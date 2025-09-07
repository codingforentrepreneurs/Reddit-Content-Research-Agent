from django.db import models

# Create your models here.
class BrightDataSnapshot(models.Model):
    snapshot_id = models.CharField(max_length=120)
    dataset_id = models.CharField(max_length=120)
    status = models.CharField(max_length=120)
    _status = models.CharField(max_length=120, blank=True, null=True)
    error_msg = models.TextField(null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    records = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    progress_check_count = models.IntegerField(default=0)
    # finished_at = models.DateTimeField(
    #     auto_now=True,
    #     auto_now_add=True,
    #     null=True, 
    #     blank=True
    # )

    @property
    def progress_complete(self):
        # snapshot is done according to bright data
        return self.status in ["ready", "failed"]


    @property
    def is_downloadable(self) -> bool:
        if self.error_msg:
            return False
        return self.status == "ready" and self.records > 0