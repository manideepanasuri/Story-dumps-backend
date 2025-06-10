import uuid
from django.db import models
from brainrot import settings

User = settings.AUTH_USER_MODEL

class TaskModel(models.Model):
    STATUS_CHOICES = [("PENDING", "PENDING"), ("SUCCESS", "SUCCESS"), ("FAILURE", "FAILURE")]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    useduuid = models.UUIDField(default=uuid.uuid4, editable=False)
    percentage=models.DecimalField(decimal_places=0, max_digits=3,default=0)
    text = models.TextField(blank=True)
    title = models.TextField(blank=False,default="Blank Title")
    status=models.CharField(choices=STATUS_CHOICES, default="PENDING", max_length=10)
    video_url = models.URLField()
    audio_url = models.URLField()
    ass_url = models.URLField()
    thumbnail_url = models.URLField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


