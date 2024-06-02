from django.urls import path
from .views import MessageAPIView

urlpatterns = [
    path('events/<int:event_id>/messages/', MessageAPIView.as_view())
]