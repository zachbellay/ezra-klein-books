from django.http import HttpResponse

from .tasks import read_rss_feed


def start_read_rss_feed_task(request):
    read_rss_feed.delay()
    return HttpResponse("Started read_rss_feed task")
