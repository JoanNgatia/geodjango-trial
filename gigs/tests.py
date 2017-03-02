import random, factory.django
from django.contrib.gis.geos import Point
from django.test import TestCase
from factory.fuzzy import BaseFuzzyAttribute
from gigs.models import Venue
# Create your tests here.


class FuzzyPoint(BaseFuzzyAttribute):
    def fuzz(self):
        return Point(random.uniform(-180.0, 180.0),
                     random.uniform(-90.0, 90.0))


class Venuefactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Venue
        django_get_or_create = ('name', 'location')

    name = 'Wembley'
    location = FuzzyPoint()


class VenueTest(TestCase):
    def test_create_venue(self):
        venue = Venuefactory()

        all_venues = Venue.objects.all()
        self.assertEqual(len(all_venues), 1)
        self.assertEqual(venue, all_venues[0])
        self.assertEqual(all_venues[0].name, 'Wembley')
