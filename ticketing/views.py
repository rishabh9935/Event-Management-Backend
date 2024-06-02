from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TicketType, Event
from .serializers import TicketTypeSerializer, TicketSerializer
import qrcode
from io import BytesIO
from django.core.mail import EmailMessage
from .models import Ticket, TicketType
from rest_framework.permissions import IsAuthenticated
import cloudinary
import cloudinary.uploader
from event_management.models import RoleManagement, Role, Event


class BookTicket(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self, request, ticket_type_id, event_id):
        user = request.user
        event = Event.objects.get(pk=event_id)
        try:
            ticket_type = TicketType.objects.get(pk=ticket_type_id)
        except TicketType.DoesNotExist:
            return Response({"error": "Ticket type not found."}, status=status.HTTP_404_NOT_FOUND)
        
        ticket = Ticket.objects.create(
            ticket_type=ticket_type,
            user=request.user,
            checked_in=False
        )

        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"Ticket ID: {ticket.id}") 
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Save QR code image to BytesIO
        qr_img_io = BytesIO()
        qr_img.save(qr_img_io, format='PNG')
        qr_img_io.seek(0)

        
        cloudinary_response = cloudinary.uploader.upload(qr_img_io, folder='ticket_qr')

        
        cloudinary_url = cloudinary_response['secure_url']

        
        ticket.qr_code = cloudinary_url
        ticket.save()

        
        email = EmailMessage(
            subject='Your Ticket QR Code',
            body='Please find your ticket QR code attached.',
            to=[request.user.email]
        )
        email.attach(f'ticket_qr_{ticket.id}.png', qr_img_io.read(), 'image/png')
        email.send()

        if user:
            RoleManagement.objects.get_or_create(event_id=event, user_id=user, role_id=Role.objects.get(role = 'attendees'))
        else:
            Response({"message" : "User not exist"})

        return Response({"message": "Ticket booked successfully."}, status=status.HTTP_201_CREATED) 


class TicketTypeDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, event_id, ticket_type_id=None):
        if ticket_type_id:
            try:
                ticket_type = TicketType.objects.get(pk=ticket_type_id, event_id=event_id)
                serializer = TicketTypeSerializer(ticket_type)
                return Response(serializer.data)
            except TicketType.DoesNotExist:
                return Response({"error": "Ticket type not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            ticket_types = TicketType.objects.filter(event_id=event_id)
            serializer = TicketTypeSerializer(ticket_types, many=True)
            return Response(serializer.data)

    def post(self, request, event_id):
        request.data['event'] = event_id
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)
                                                                                            
        serializer = TicketTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(event=event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserBookings(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        bookings = Ticket.objects.filter(user=user).select_related('ticket_type', 'ticket_type__event')
        serializer = TicketSerializer(bookings, many=True)
        return Response(serializer.data)




















































    # def put(self, request, event_id, ticket_type_id):
    #     request.data['event'] = event_id
    #     try:
    #         ticket_type = TicketType.objects.get(pk=ticket_type_id, event_id=event_id)
    #     except TicketType.DoesNotExist:
    #         return Response({"error": "Ticket type not found."}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = TicketTypeSerializer(ticket_type, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, event_id, ticket_type_id):
    #     try:
    #         ticket_type = TicketType.objects.get(pk=ticket_type_id, event_id=event_id)
    #     except TicketType.DoesNotExist:
    #         return Response({"error": "Ticket type not found."}, status=status.HTTP_404_NOT_FOUND)

    #     ticket_type.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


