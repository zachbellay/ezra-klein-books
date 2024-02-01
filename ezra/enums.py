from django.db import models


class WhisperModelSize(models.TextChoices):
    TINY = "tiny", "tiny"
    BASE = "base", "base"
    SMALL = "small", "small"
    MEDIUM = "medium", "medium"
    LARGE = "large", "large"
