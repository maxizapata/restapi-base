from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Trip, TypeOfVehicle, Vehicle


@admin.register(Trip)
class TripAdmin(ModelAdmin):
    fields = (
        'pick_up',
        'drop_off',
        'rider',
    )
    list_display = (
        'uuid',
        'pick_up',
        'drop_off',
        'driver',
        'rider',
        'created_at',
        'updated_at',
        'status'
    )


@admin.register(TypeOfVehicle)
class TypeOfVehicleAdmin(ModelAdmin):
    fields = (
        'vehicle_type',
        'vehicle_type_name',
        'max_weight',
        'picture',
    )
    list_display = (
        'vehicle_type',
        'vehicle_type_name',
        'max_weight',
        'picture',
    )


@admin.register(Vehicle)
class VehicleAdmin(ModelAdmin):
    fields = (
        'driver',
        'license_plate',
        'make',
        'model',
        'year',
        'vehicle_type',
        'price_per_hour'
    )
    list_display = (
        'driver',
        'license_plate',
        'model',
        'make',
        'year',
        'vehicle_type',
        'price_per_hour'
    )