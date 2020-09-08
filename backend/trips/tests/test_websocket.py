from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import Client
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
import pytest
from rest_framework_simplejwt.tokens import RefreshToken
from core.routing import application
from trips.models import Trip
from shared.jwt_functions import get_jwt_token
from accounts.tests.test_http import (create_user,
                                      EMAIL,
                                      PASSWORD)


@database_sync_to_async
def create_user(username=EMAIL, password=PASSWORD, role=1):
    return get_user_model().objects.create_user(
        username=username,
        email=username,
        password=password,
        mobile='+5491124004759',
        role=role,
        verified_mobile=False
    )


TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


async def authorized_user_can_connect(role,
                                      settings,
                                      func=None,
                                      vehicle=None):
    settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    user = await create_user(
        EMAIL, PASSWORD, role=role
    )

    token = get_jwt_token(user)['access']

    if vehicle:
        path = f'ws/trips/?token={token}&vehicle={vehicle}'
    else:
        path = f'ws/trips/?token={token}'

    communicator = WebsocketCommunicator(
        application=application,
        path=path
    )

    connected, _ = await communicator.connect()

    if func:
        func()
    else:
        assert connected is True

    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestWebsockets:

    async def test_authorized_rider_can_connect(self, settings):
        await authorized_user_can_connect(2, settings)

    async def test_authorized_driver_can_connect(self, settings):
        await authorized_user_can_connect(1, settings, vehicle='camioneta')

