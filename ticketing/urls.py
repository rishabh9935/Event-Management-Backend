from django.urls import path
from .views import TicketTypeDetail, BookTicket, UserBookings


urlpatterns = [
    path('events/<int:event_id>/create-ticket-type/', TicketTypeDetail.as_view(), name='create_ticket_type'),
    path('events/<int:event_id>/ticket-types/', TicketTypeDetail.as_view(), name='ticket_type_detail'),
    path('events/<int:event_id>/ticket-types/<int:ticket_type_id>/', TicketTypeDetail.as_view(), name='ticket_type_detail'),
    # path('tickettypes/<int:pk>/', TicketTypeView.as_view(), name='tickettype'),
    path('events/<int:event_id>/ticket-types/<int:ticket_type_id>/book/', BookTicket.as_view(), name='book_ticket'),
    path('user-bookings/', UserBookings.as_view(), name='user_bookings'),
]

