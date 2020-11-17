from channels.generic.websocket import JsonWebsocketConsumer
import json
from asgiref.sync import async_to_sync


class MealPointConsumer(JsonWebsocketConsumer):
    groups = ['mealpoint']

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("mealpoint", self.channel_name)

    def mealpoint_message(self, event):
        self.send_json(event['data'])
