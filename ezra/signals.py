from django.db.models.signals import pre_save

from ezra.models import PodcastEpisode
from ezra.utils import unique_slug_generator


def podcast_episode_presave_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        if isinstance(instance, PodcastEpisode):
            print('pre_save signal received')
            instance.slug = unique_slug_generator(
                instance, "title"
            )

pre_save.connect(podcast_episode_presave_receiver, sender=PodcastEpisode)
