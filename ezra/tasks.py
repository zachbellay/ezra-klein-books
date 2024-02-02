import re
import tempfile

import bleach
import dateparser
import feedparser
import mutagen
import requests
from celery import shared_task

from ezra.models import PodcastEpisode


def clean_description(text: str) -> str:
    # remove urls that are inside [], e.g. [https://www.example.com]
    text = re.sub(r"\[https?://[^\]]+\]", "", text)

    # linkify naked urls
    text = bleach.linkify(text)

    # remove unsafe tags
    text = bleach.clean(
        text, tags=list(bleach.sanitizer.ALLOWED_TAGS) + ["p"], strip=True
    )

    return text


def duration_to_seconds(duration_str):
    try:
        # Try to parse the duration string as an integer
        duration_in_seconds = int(duration_str)
    except ValueError:
        duration_in_seconds = 0
        for part in duration_str.split(":"):
            duration_in_seconds = duration_in_seconds * 60 + int(part, 10)

    return duration_in_seconds


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0"
}


@shared_task
def read_rss_feed():
    EZRA_KLEIN_RSS_FEED = "https://feeds.simplecast.com/82FI35Px"

    feed = feedparser.parse(EZRA_KLEIN_RSS_FEED)

    for entry in feed.entries:
        audio_url = None
        for link in entry.links:
            if link.type == "audio/mpeg":
                audio_url = link.href
                break

        duration = duration_to_seconds(entry.itunes_duration)

        try:
            resolved_request = requests.head(
                audio_url, headers=headers, allow_redirects=True
            )

            print(f"Resolved audio url: {resolved_request.url}")
        except requests.exceptions.TooManyRedirects:
            print(f"Too many redirects: {audio_url}")
            continue

        print(f"Title: {entry.title}")
        print(f"Audio url: {audio_url}")
        print(f"Resolved audio url: {resolved_request.url}")
        print(f"Duration: {duration}")
        print(f"Description: {entry.description}")
        episode = PodcastEpisode.objects.create(
            title=entry.title,
            description=clean_description(entry.description),
            date=dateparser.parse(entry.published),
            audio_url=audio_url,
            resolved_audio_url=resolved_request.url,
            details_url=audio_url,
            duration=duration,
        )
        print(episode)

        r = requests.get(episode.resolved_audio_url)
        audio_data = r.content

        f = tempfile.NamedTemporaryFile()
        f.write(audio_data)

        duration = int(mutagen.File(f.name).info.length)

        break


# date = models.DateTimeField(null=False)
# title = models.CharField(max_length=200, null=False)
# description = models.TextField(null=False)
# details_url = models.CharField(max_length=2048, null=False, blank=False)
# slug = models.SlugField(max_length=250, null=True, blank=True)

# # transcription & audio information
# audio_url = models.CharField(max_length=2048, null=False, blank=False)
# resolved_audio_url = models.CharField(max_length=2048, null=False, blank=False)
# transcription = models.JSONField(default=None, null=True, blank=True)
# transcription_full_text = models.TextField(blank=True, default=None, null=True)
# whisper_model_size = models.CharField(
# max_length=10,
# choices=WhisperModelSize.choices,
# default=WhisperModelSize.BASE,
# )
# whisper_transcription_object = models.JSONField(default=None, null=True, blank=True)
# duration = models.PositiveIntegerField(default=None, null=True, blank=True)
