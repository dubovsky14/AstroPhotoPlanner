from django.db import models

# Create your models here.

# user profile model to store user preferences
class UserProfile(models.Model):
    name = models.CharField(max_length=40)
    gps_lat = models.FloatField()
    gps_lon = models.FloatField()
    astronomical_night_angle_limit = models.FloatField(default=-18.0)  # default to astronomical night
    minimal_target_angle_above_horizon = models.FloatField(default=30.0)
