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
    bg_video_url=models.URLField(blank=True)
    speed=models.DecimalField(decimal_places=1, max_digits=2,default=1)
    voice=models.CharField(max_length=100,default='af_heart')
    status=models.CharField(choices=STATUS_CHOICES, default="PENDING", max_length=10)
    video_url = models.URLField()
    audio_url = models.URLField()
    ass_url = models.URLField()
    thumbnail_url = models.URLField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class BackGroundModel(models.Model):
    video_url = models.URLField(blank=False)
    image_url=models.URLField(blank=False,default="")
    def __str__(self):
        return self.video_url

class VoiceModel(models.Model):
    voice = models.CharField(max_length=100,blank=False)
    voice_url = models.URLField(blank=False,default="")
    def __str__(self):
        return self.voice