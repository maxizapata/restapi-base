from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from urllib.parse import parse_qs
from .models import Trip
from .serializers import TripSerializer, NestedTripSerializer
from .models import User


class TripConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        if user.is_anonymous:
            await self.close()
            exit()
        if user.role == 1:
            # Enter if role is driver and add to vehicle group
            vehicle = parse_qs(
                self.scope['query_string'].decode(
                    'utf8'))['vehicle'][0]
            await self.channel_layer.group_add(
                group=vehicle,
                channel=self.channel_name
            )
        await self._save_channel_name(user)
        await self.accept()

    async def receive_json(self, content):
        '''
        When the the rider created trip, data is the input data,
        after that, data is the output of trip_data
        '''
        user = self.scope['user']
        message_type = content['type']
        rider = content['data']['rider']['id']
        driver = content['data']['driver']['id']
        if message_type == 'create.trip':
            await self.create_trip(content)
        elif message_type == 'driver_available':
            await self.send_message(rider, content['data'])
        elif message_type == 'confirm_driver':
            # Selected driver will be disconnected
            self.disconnect_user()



    async def create_trip(self, content):
        data = content['data']
        role = self.scope['user'].role
        if role == 2:
            trip = await self._create_trip(data)
            trip_data = NestedTripSerializer(trip)
            await self.send_group_message(data['vehicle'], trip_data)

    async def echo_message(self, message):
        await self.send_json(message['data'])

    async def disconnect_user(self, user_id, group):
        self.channel_layer.group_discard(
            group=group,
            channel=self._get_channel_name(user.id)
        )

    async def send_group_message(self, group, message):
        await self.channel_layer.group_send(
            group=group, message={
                'type': 'echo.message',
                'data': message
            }
        )

    async def send_message(self, user_id, message):
        channel_name = self._get_channel_name(user_id)
        await self.channel_layer.send(
            channel_name=channel_name,
            message={
                'type': 'echo.message',
                'data': message
            }
        )

    # Sync methods
    @database_sync_to_async
    def _create_trip(self, data):
        role = self.scope['user'].role
        if role == 2:
            serializer = TripSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            trip = serializer.create(serializer.validated_data)
            return trip

    @database_sync_to_async
    def _get_channel_name(self, user_id):
        user = User.objects.get(pk=user_id)
        return user.channel_name

    @database_sync_to_async
    def _save_channel_name(self, user):
        user.channel_name = self.channel_name
        user.save()

        # queda pendiente desconectar el condutor para conectarlo en la nueva clase



