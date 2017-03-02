from __future__ import unicode_literals

from django.contrib.gis.db import models


# Create your models here.
class Venue(models.Model):
    name = models.CharField(max_length=200)
    location = models.PointField()
