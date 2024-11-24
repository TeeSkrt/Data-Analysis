# backend/routing.py

from django.urls import re_path
from base.consumers import BaseConsumer

websocket_urlpatterns = [
    re_path(r'ws/base/$', BaseConsumer.as_asgi()),
]
