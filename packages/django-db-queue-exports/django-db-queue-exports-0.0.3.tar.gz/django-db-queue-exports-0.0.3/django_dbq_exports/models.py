from django.db import models
from django_dbq.models import Job
from jsonfield import JSONField
from model_utils import Choices
import uuid


class Export(models.Model):
    class STATUS:
        QUEUED = "QUEUED"
        RUNNING = "RUNNING"
        COMPLETE = "COMPLETE"
        FAILED = "FAILED"

    STATUS_CHOICES = Choices(
        (STATUS.QUEUED, "QUEUED"),
        (STATUS.RUNNING, "RUNNING"),
        (STATUS.COMPLETE, "COMPLETE"),
        (STATUS.FAILED, "FAILED"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)
    started = models.DateTimeField(null=True)
    completed = models.DateTimeField(null=True)
    export_type = models.CharField(max_length=256, null=False)
    priority = models.SmallIntegerField(default=1, db_index=True, null=False)
    status = models.CharField(
        max_length=24,
        choices=STATUS_CHOICES,
        default=STATUS.QUEUED,
        db_index=True,
        null=False,
    )
    status_detail = models.CharField(max_length=2048, null=True)
    result_reference = models.CharField(max_length=2048, null=True)
    export_params = JSONField(null=True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"{self.id}"

    def save(self, *args, **kwargs):
        is_new = not Export.objects.filter(pk=self.pk).exists()

        if is_new:
            Job.objects.create(
                name="export", workspace={"export_id": self.id}, priority=self.priority
            )

        return super(Export, self).save(*args, **kwargs)

    def update_status(self, status, detail=None):
        self.status = status
        self.status_detail = detail[:2048] if detail else None
        self.save()

    @property
    def runtime(self):
        if self.started and self.completed:
            return (self.completed - self.started).total_seconds()
        return None
