from django.urls import path # type: ignore
from .views import (
    HandleAttendeeResponse, InviteAttendees, RegisterUser, LoginUser, EventList, 
    EventView,SearchEventsView, ForgotPasswordAPIView, ResetPasswordAPIView, LogoutUser, 
    AddEmailsToRole, RoleAPIView, GetCurrentUser, AddDonorAPIView, SilentAuctionView, HighestBidView, 
    RandomRaffleView, DonorListCreateAPIView, CheckAuthView, HostOfTheEvent, ChangePassword, EventViewSet, ExpiredEventsAPIView)
from django.contrib.auth import views as auth_views # type: ignore
from rest_framework.routers import DefaultRouter  # type: ignore

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')


urlpatterns = [
    path('api/register/', RegisterUser.as_view(), name='register'),
    path('api/login/', LoginUser.as_view(), name='login'),
    path('api/logout/', LogoutUser.as_view(), name='logout'),
    path('api/events/', EventList.as_view(), name='event-list'),
    path('check-auth/', CheckAuthView.as_view(), name='check_auth'),
    path('api/expired-events/', ExpiredEventsAPIView.as_view(), name='expired-events'),
    # path('api/events/<int:event_id>/', GetEventView.as_view(), name='get_event'),
    # path('api/events/post/', PostEventView.as_view(), name='post_event'),
    # path('api/events/<int:event_id>/', EventView.as_view(), name='event-detail'),
    # path('api/events/post/', EventView.as_view(), name='event-create'),
    # path('api/events/<int:event_id>/update/', EventView.as_view(), name='event-update'),
    # path('api/events/<int:event_id>/delete/', EventView.as_view(), name='event-delete'),
    path('api/events/search/', SearchEventsView.as_view(), name='search_events'),
    # path('reset_password', auth_views.PasswordResetView.as_view(), name='reset_password'),
    # path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('api/events/<int:event_id>/addRole/', AddEmailsToRole.as_view(), name='adding-role'),
    path('api/events/<int:event_id>/delRole/<str:username>/', AddEmailsToRole.as_view(), name='delete-role'),
    path('events/<int:event_id>/role/', RoleAPIView.as_view(), name='event-role'),
    path('events/<int:event_id>/invite-attendees/', InviteAttendees.as_view(), name='invite_attendees'),
    path('events/<int:event_id>/handle-response/<str:email>/', HandleAttendeeResponse.as_view(), name='handle_response'),
    path('api/getUser/', GetCurrentUser.as_view(), name='get_current_user'),
    path('donor/', AddDonorAPIView.as_view(), name='donor'),
    path('donorsInvite/', DonorListCreateAPIView.as_view(), name='donor-list-create'),
    path('events/<int:event_id>/bid/',SilentAuctionView.as_view(),name='bid-item'),
    path('events/<int:event_id>/highestbid/', HighestBidView.as_view(),name='high-bid'),
    path('events/<int:event_id>/raffle/', RandomRaffleView.as_view(),name='raffle'),
    path('events/<int:event_id>/host/', HostOfTheEvent.as_view(), name='event-host'),
    path('api/change_password/', ChangePassword.as_view(), name='change_password'),
] + router.urls