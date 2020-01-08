from django.urls import path
from . import consumer

ws_url_pattern = [
    path('ws', consumer.LatexConsumer),
]

