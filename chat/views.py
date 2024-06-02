from rest_framework.response import Response
from rest_framework.views import APIView
from .pusher import pusher_client
from .serializers import MessageSerializer
from .models import Messages
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from event_management.models import Event

class MessageAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, event_id):
        event_message = Messages.objects.filter(event=event_id).select_related('user')
        serializer = MessageSerializer(event_message, many=True)
        return Response(serializer.data)

    def post(self, request, event_id):
        username = request.user.username
        event = Event.objects.get(pk=event_id)
        serializer = MessageSerializer(data=request.data)
        # serializer = MessageSerializer(data={'user': request.user.id, 'message':request.data.get('message'), 'event': event_id})
        if serializer.is_valid():
            serializer.save(user = request.user, event=event)
            # serializer.save()
            pusher_client.trigger('chat', 'message', {
                'username': username,
                'message': serializer.data.get('message')
            })
            return Response("Message sent succefully", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)