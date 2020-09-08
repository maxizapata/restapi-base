from django.db import models
from accounts.models import User
import uuid
from datetime import datetime

# Create your models here.
INITIAL_YEAR = 1980
CURRENT_YEAR = datetime.now().year + 1


def gen_years():
    years = []
    for y in range(INITIAL_YEAR, CURRENT_YEAR):
        years.append((str(y), y))
    return years


YEAR_CHOICES = gen_years()


class TypeOfVehicle(models.Model):
    vehicle_type = models.CharField(max_length=50)
    vehicle_type_name = models.CharField(max_length=50)
    max_weight = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='.', default='./photo.png')

    def __str__(self):
        return str(self.vehicle_type)


class Trip(models.Model):
    REQUESTED = 'REQUESTED'
    STARTED = 'STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    STATUSES = (
        (REQUESTED, REQUESTED),
        (STARTED, STARTED),
        (IN_PROGRESS, IN_PROGRESS),
        (COMPLETED, COMPLETED),
    )
    pick_up = models.CharField(max_length=200)
    drop_off = models.CharField(max_length=200)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    driver = models.OneToOneField(User,
                                  on_delete=models.DO_NOTHING,
                                  null=True,
                                  related_name='driver',
                                  blank=True,
                                  limit_choices_to={'role': 1})
    rider = models.OneToOneField(User,
                                 on_delete=models.DO_NOTHING,
                                 null=True, related_name='rider',
                                 limit_choices_to={'role': 2})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, choices=STATUSES, default=REQUESTED
    )

    def __str__(self):
        return str(self.uuid)


class Vehicle(models.Model):
    driver = models.ForeignKey(User,
                               on_delete=models.DO_NOTHING,
                               limit_choices_to={'role': 2})
    vehicle_type = models.ForeignKey(TypeOfVehicle,
                                     on_delete=models.DO_NOTHING)
    year = models.CharField(max_length=20,
                            choices=YEAR_CHOICES,
                            default=INITIAL_YEAR)
    is_active = models.BooleanField(default=False)
    license_plate = models.CharField(max_length=20, blank=True)
    model = models.CharField(max_length=50, blank=True)
    make = models.CharField(max_length=20)
    price_per_hour = models.DecimalField(max_digits=9999,
                                         decimal_places=2,
                                         blank=False,
                                         null=False)

    def __str__(self):
        return str(self.license_plate)