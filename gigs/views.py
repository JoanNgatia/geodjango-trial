from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
# from django.views.generic import View
from django.views.generic.edit import FormView
from gigs.forms import LookupForm
from gigs.models import Event


# Create your views here.
class LookUpView(FormView):
    form_class = LookupForm

    def get(self, request):
        return render_to_response('gigs/lookup.html', RequestContext(request))

    def form_valid(self, form):
        # import ipdb; ipdb.set_trace()
        latitude = form.cleaned_data['latitude']
        longitude = form.cleaned_data['longitude']

        now = timezone.now()

        next_week = now + timezone.timedelta(weeks=1)

        location = Point(longitude, latitude, srid=4326)

        events = Event.objects.filter(datetime__gte=now).filter(datetime__lte=next_week).annotate(distance=Distance('venue__location', location)).order_by('distance')[0:5]

        return render_to_response('gigs/lookupresults.html', {'events': events})
