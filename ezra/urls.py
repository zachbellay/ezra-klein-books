from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

from . import views

urlpatterns = [
    path(
        "read-rss-feed/",
        views.start_read_rss_feed_task,
        name="start_read_rss_feed_task",
    ),
]
