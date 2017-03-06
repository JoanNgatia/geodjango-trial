from django.conf.urls import url
from gigs.views import LookUpView

urlpatterns = [
    url(r'', LookUpView.as_view(), name='lookup'),
]
