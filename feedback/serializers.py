from rest_framework import serializers
from .models import Feedback
from event_management.serializers import EventSerializer, UserSerializer

# class FeedbackSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='user.username', required=False, max_length=255)
#     class Meta:
#         model = Feedback
#         fields = ['id', 'event', 'user', 'username', 'rating', 'comment']



class FeedbackSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    event = EventSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    username = serializers.CharField(source='user.username', required=False, max_length=255)
    rating = serializers.IntegerField()
    comment = serializers.CharField()

    def create(self, validated_data):
        return Feedback.objects.create(**validated_data)