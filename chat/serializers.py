from rest_framework import serializers
from .models import Messages
from event_management.serializers import UserSerializer, EventSerializer


# class MessageSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='user.username', required=False, max_length=255)
#     class Meta:
#         model = Messages
#         fields = ['id', 'message', 'username', 'user', 'event']
    

class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True, required=False, max_length=255)
    message = serializers.CharField()
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)

    def create(self, validated_data):
        return Messages.objects.create(**validated_data)


