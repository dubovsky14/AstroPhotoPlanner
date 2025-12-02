from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# user profile model to store user preferences
class UserProfile(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=40)
    gps_lat = models.FloatField()
    gps_lon = models.FloatField()
    astronomical_night_angle_limit = models.FloatField(default=-18.0)  # default to astronomical night
    minimal_target_angle_above_horizon = models.FloatField(default=30.0)

class Catalogue(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='catalogues')

    def __str__(self):
        return f"{self.name} (Owner: {self.owner.name})"

class DeepSkyObject(models.Model):
    catalogue = models.ForeignKey(Catalogue, on_delete=models.CASCADE, related_name="objects")
    name = models.CharField(max_length=100)
    ra = models.FloatField()  # Right Ascension in degrees
    dec = models.FloatField()  # Declination in degrees
    magnitude = models.FloatField(null=True, blank=True)
    object_type = models.CharField(max_length=50, blank=True)
    plan_to_photograph = models.BooleanField(default=True)

class Location(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='locations')
    gps_lat = models.FloatField()
    gps_lon = models.FloatField()
    description = models.TextField(blank=True)