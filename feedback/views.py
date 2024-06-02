from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Feedback
from .serializers import FeedbackSerializer
from rest_framework.permissions import IsAuthenticated 
from event_management.models import CustomUser
from event_management.models import Event

class FeedbackView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, event_id):
        user = request.user
        event = Event.objects.get(pk=event_id)
        request.data['event'] = event_id
        request.data['user'] = request.user.id
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user, event=event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, event_id):
        request.data['event'] = event_id
        request.data['user'] = request.user.id
        # feedback = Feedback.objects.all()
        feedback = Feedback.objects.all().select_related('user')
        serializer = FeedbackSerializer(feedback, many=True)
        return Response(serializer.data)

    # def put(self, request, pk):
    #     try:
    #         feedback = Feedback.objects.get(pk=pk)
    #     except Feedback.DoesNotExist:
    #         return Response({"error": "Feedback not found."}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = FeedbackSerializer(feedback, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk):
    #     try:
    #         feedback = Feedback.objects.get(pk=pk)
    #     except Feedback.DoesNotExist:
    #         return Response({"error": "Feedback not found."}, status=status.HTTP_404_NOT_FOUND)

    #     feedback.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)



