from django.urls import path
from social.views.analytics_view import AnalyticsView

urlpatterns = [
    path('', AnalyticsView.as_view(), name='analytics'),
]