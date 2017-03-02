from django.contrib import admin
from django.forms import ModelForm
from floppyforms.gis import PointWidget, BaseGMapWidget
from models import Venue, Event


class CustomPointWidget(PointWidget, BaseGMapWidget):
    class Media:
        js = ('floppyforms/js/MapWidget.js',)


class VenueAdminForm(ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'location']
        widgets = {
            'location': CustomPointWidget()
        }


class VenueAdmin(admin.ModelAdmin):
    form = VenueAdminForm


# Register your models here.
admin.site.register(Venue, VenueAdmin)
admin.site.register(Event)
