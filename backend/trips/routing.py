from django.urls import path
from .consumers import TripConsumer

trips_ws_urlpatterns = [
    path('ws/trips/', TripConsumer)
]
