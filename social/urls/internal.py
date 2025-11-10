from django.urls import path
from social.views.internal_events_view import InternalEventsView

urlpatterns = [
    path('events', InternalEventsView.as_view(), name='internal-events'),
]