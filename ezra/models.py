from django.db import models
from shortuuidfield import ShortUUIDField

from .enums import WhisperModelSize


class BaseModel(models.Model):
    class Meta:
        abstract = True

    uid = ShortUUIDField(primary_key=True, editable=False, max_length=10)
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)


class PodcastEpisode(BaseModel):
    # podcast information
    date = models.DateTimeField(null=False)
    title = models.CharField(max_length=200, null=False)
    description = models.TextField(null=False)
    details_url = models.CharField(max_length=2048, null=False, blank=False)
    slug = models.SlugField(max_length=250, null=True, blank=True)

    # transcription & audio information
    audio_url = models.CharField(max_length=2048, null=False, blank=False)
    resolved_audio_url = models.CharField(max_length=2048, null=False, blank=False)
    transcription = models.JSONField(default=None, null=True, blank=True)
    transcription_full_text = models.TextField(blank=True, default=None, null=True)
    whisper_model_size = models.CharField(
        max_length=10,
        choices=WhisperModelSize.choices,
        default=WhisperModelSize.BASE,
    )
    whisper_transcription_object = models.JSONField(default=None, null=True, blank=True)
    duration = models.PositiveIntegerField(default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.date} - {self.title}"
