import random
import factory.django
from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.utils import timezone
from factory.fuzzy import BaseFuzzyAttribute
from gigs.models import Venue, Event
from gigs.views import LookUpView
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


class Eventfactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event
        django_get_or_create = ('name', 'venue', 'datetime')

    name = 'Mkahawa the Kahawas'
    datetime = timezone.now()


class VenueTest(TestCase):
    def test_create_venue(self):
        venue = Venuefactory()

        all_venues = Venue.objects.all()
        self.assertEqual(len(all_venues), 1)
        self.assertEqual(venue, all_venues[0])
        self.assertEqual(all_venues[0].name, 'Wembley')


class EventsTest(TestCase):
    def test_create_event(self):
        venue = Venuefactory()

        event = Eventfactory(venue=venue)

        all_events = Event.objects.all()
        self.assertEqual(len(all_events), 1)
        self.assertEqual(event, all_events[0])
        self.assertIn('Mkahawa', all_events[0].name)
        self.assertEqual(all_events[0].venue.name, 'Wembley')


class LookupViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get(self):
        request = self.factory.get(reverse('lookup'))
        response = LookUpView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('gigs/lookup.html')
