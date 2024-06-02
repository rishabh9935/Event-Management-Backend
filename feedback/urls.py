from django.urls import path
from .views import FeedbackView

urlpatterns = [
    path('events/<int:event_id>/feedback/', FeedbackView.as_view(), name='feedback-list'),
    path('feedback/<int:pk>/', FeedbackView.as_view(), name='feedback-detail'),
]