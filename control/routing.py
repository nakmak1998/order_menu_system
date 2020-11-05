from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/dist', consumers.MealPointConsumer.as_asgi()),
]