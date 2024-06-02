from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.permissions import IsAuthenticated   # type: ignore
from rest_framework import status #type: ignore
from rest_framework.permissions import AllowAny #type: ignore
from .serializers import UserSerializer, EventSerializer, DonorSerializer, SilentAuctionSerializer
from django.contrib.auth import authenticate, login #type: ignore
from rest_framework_simplejwt.tokens import RefreshToken #type: ignore
from .models import CustomUser, RoleManagement, Role, Event, DonorManagement, Donor, Auction 
from django.http import JsonResponse #type: ignore
from django.shortcuts import get_object_or_404 #type: ignore
from django.core.mail import send_mail #type: ignore
from django.contrib.auth.models import User #type: ignore
from .models import CustomUser
from django.urls import reverse #type: ignore
from rest_framework.views import APIView #type: ignore
from django.contrib.auth import get_user_model #type: ignore
from django.utils.http import urlsafe_base64_encode #type: ignore
from django.contrib.auth.tokens import default_token_generator #type: ignore
from django.utils.http import urlsafe_base64_decode #type: ignore
from django.utils.encoding import force_bytes #type: ignore
from cloudinary import uploader #type: ignore
from django.contrib.auth import logout #type: ignore
from .permissions import IsHost, IsVolunteer, IsOrganiser, IsAttendee, isEventPart #type: ignore
from django.http import JsonResponse #type: ignore
import random
import json
from drf_yasg import openapi #type: ignore 
from drf_yasg.utils import swagger_auto_schema #type: ignore
from rest_framework import viewsets #type: ignore
from rest_framework.pagination import LimitOffsetPagination

class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        if serializer.is_valid():
            serializer.save()
            subject = 'About Registration'
            message = f'Hi {username}, You are registered successfully.'
            email_from = 'rishabhagarwal9935@gmail.com'
            rec_list = [email,]
            send_mail(subject, message, email_from, rec_list)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password'],
        ),
        responses={200: 'Login successful', 401: 'Invalid credentials'},
        security=[{'Bearer': []}]
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login(request, user)
            refresh = RefreshToken.for_user(user)
            response = Response({'message': 'Login successful', 'access': str(refresh.access_token)})
            response.set_cookie(key='access_token' ,value=str(refresh.access_token))
            response.set_cookie(key='refresh_token', value=str(refresh))
            return response
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class LogoutUser(APIView):
    def post(self, request):
        print(request.user)
        # logout(request)
        response = Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        print(request.user)
        return response

class ExpiredEventsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            expired_events = Event.objects.expired().filter(id__gte=10)
            serializer = EventSerializer(expired_events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventList(APIView):
    def get(self, request):
        events = Event.objects.all()
        data = []
        for event in events:
            if event.is_private:
                if(isEventPart().has_permission(request=request,event=event ,view=self)):
                    data += [{
                    'id': event.id,
                    'name': event.name,
                    'date': event.date,
                    'location': event.location,
                    'description': event.description,
                    'image_urls': event.image_urls,
                    'photo' : str(event.photo.url if event.photo else None)}]
            else:
                data += [{
                    'id': event.id,
                    'name': event.name,
                    'date': event.date,
                    'location': event.location,
                    'description': event.description,
                    'image_urls': event.image_urls,
                    'photo' : str(event.photo.url if event.photo else None)}]
        return JsonResponse({'events' : data})

class CheckAuthView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({"isAuthenticated": True, "user": {"username": request.user.username}})
        else:
            return Response({"isAuthenticated": False})
        


class EventViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        if self.request.method == 'DELETE':
            return [IsAuthenticated()]
        if self.request.method == 'UPDATE':
            return [IsAuthenticated()]
        else:
            return [AllowAny()]
        
    pagination_class = LimitOffsetPagination

    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def list(self, request):
        queryset = Event.objects.all()
        page = self.paginate_queryset(queryset)
        print(page)
        
        data = []
        events = page if page is not None else queryset

        for event in events:
            if event.is_private:
                if(isEventPart().has_permission(request=request,event=event ,view=self)):
                    data += [{
                    'id': event.id,
                    'name': event.name,
                    'date': event.date,
                    'location': event.location,
                    'description': event.description,
                    'image_urls': event.image_urls,
                    'photo' : str(event.photo.url if event.photo else None)}]
            else:
                data += [{
                    'id': event.id,
                    'name': event.name,
                    'date': event.date,
                    'location': event.location,
                    'description': event.description,
                    'image_urls': event.image_urls,
                    'photo' : str(event.photo.url if event.photo else None)}]
        if page is not None:
            return self.get_paginated_response(data)
        
        return Response({'events': data})


    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        event = get_object_or_404(Event, pk=pk)
        photo_url = event.photo.url if event.photo else None
        data = {
            'id': event.id,
            'name': event.name,
            'date': event.date,
            'location': event.location,
            'description': event.description,
            'details' : event.details,
            'is_private' : event.is_private,
            'is_raffle' : event.is_raffle,
            'bidItem' : event.bidItem,
            'photo' : str(photo_url),
            'image_urls': event.image_urls
        }
        return JsonResponse(data)

    def create(self, request):
        serializer = EventSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            image_file = request.FILES.get('photo')
            
            try:
                images = request.FILES.getlist('images')
                cloudinary_urls = []
                for image in images:
                    result = uploader.upload(image, folder='event_images')
                    image_url = result['secure_url']
                    cloudinary_urls.append(image_url)

                serializer.validated_data['image_urls'] = json.dumps(cloudinary_urls)

                cloudinary_response = uploader.upload(image_file, folder='event_images')
                # print(cloudinary_response['secure_url'])
                print(serializer.validated_data)
                event = serializer.save(photo=cloudinary_response['secure_url'])
                # print(event)
                host_role = Role.objects.get(role='host')
                host = CustomUser.objects.get(pk=request.user.id)
                RoleManagement.objects.create(event_id=event, user_id=host, role_id=host_role)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, **kwargs):
        pk = self.kwargs.get('pk')
        event = get_object_or_404(Event, pk=pk)
        if not IsHost().has_permission(request=request, event=event, view=self):
                return Response({"error": "You don't have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, **kwargs):
        pk = self.kwargs.get('pk')
        event = get_object_or_404(Event, pk=pk)
        if not IsHost().has_permission(request=request, event=event, view=self):
                return Response({"error": "You don't have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        event.delete()
        return Response({"message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class EventView(APIView):
    # permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        else:
            return [AllowAny()]
    
    def get(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        photo_url = event.photo.url if event.photo else None
        data = {
            'id': event.id,
            'name': event.name,
            'date': event.date,
            'location': event.location,
            'description': event.description,
            'details' : event.details,
            'is_private' : event.is_private,
            'is_raffle' : event.is_raffle,
            'bidItem' : event.bidItem,
            'photo' : str(photo_url),
            'image_urls': event.image_urls
        }
        return JsonResponse(data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            image_file = request.FILES.get('photo')
            
            try:
                images = request.FILES.getlist('images')
                cloudinary_urls = []
                for image in images:
                    result = uploader.upload(image, folder='event_images')
                    image_url = result['secure_url']
                    cloudinary_urls.append(image_url)

                serializer.validated_data['image_urls'] = json.dumps(cloudinary_urls)

                cloudinary_response = uploader.upload(image_file, folder='event_images')
                # print(cloudinary_response['secure_url'])
                print(serializer.validated_data)
                event = serializer.save(photo=cloudinary_response['secure_url'])
                # print(event)
                host_role = Role.objects.get(role='host')
                host = CustomUser.objects.get(pk=request.user.id)
                RoleManagement.objects.create(event_id=event, user_id=host, role_id=host_role)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        if not IsHost().has_permission(request=request, event=event, view=self):
                return Response({"error": "You don't have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        if not IsHost().has_permission(request=request, event=event, view=self):
                return Response({"error": "You don't have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        event.delete()
        return Response({"message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    



class SearchEventsView(APIView):
    def get(self, request):
        search_query = request.GET.get('q')
        events = Event.objects.filter(name__icontains=search_query)      
        
        data = [{
            'id': event.id,
            'name': event.name,
            'date': event.date,
            'location': event.location,
            'description': event.description,
            'image_urls': event.image_urls,
            'photo' : str(event.photo.url if event.photo else None)
        } for event in events]
        
        return JsonResponse(data, safe=False)


# CustomUser = get_user_model()

class ForgotPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if email:
            # user = CustomUser.objects.filter(email=email)
            user = CustomUser.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                frontend_url = f'http://localhost:3000/reset-password/'
                reset_link = frontend_url + f'{urlsafe_base64_encode(force_bytes(user.pk))}/{token}/'
                # reset_link = request.build_absolute_uri(reverse('reset-password')) + f'?uidb64={urlsafe_base64_encode(force_bytes(user.pk))}&token={token}'
                send_mail(
                    'Password Reset',
                    f'Click this link to reset your password: {reset_link}',
                    'rishabhagarwal9935@gmail.com',
                    [email],
                    fail_silently=False,
                )
                return Response({'message': 'Password reset link sent successfully.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Email not found.'}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordAPIView(APIView):
    def post(self, request):
        uidb64 = request.data.get('uidb64')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        if uidb64 and token and new_password:
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = CustomUser.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
                user = None
            
            if user and default_token_generator.check_token(user, token):
                # Update password
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid token or missing data.'}, status=status.HTTP_400_BAD_REQUEST)

class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        if old_password == new_password:
            return Response({'error': 'New password must be different from old password'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


class HostOfTheEvent(APIView):
    def get(self, request, event_id):
        try:
            # host_role = RoleManagement.objects.filter(event_id=event_id, role_id__role = 'host')
            host_role = RoleManagement.objects.filter(event_id=event_id, role_id__role = 'host').first()
            if host_role:
                serializer = UserSerializer(host_role.user_id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Host not found for the event'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class AddEmailsToRole(APIView):
    def post(self, request, event_id):
        role_name = request.data.get('role')
        email_addresses = request.data.get('emails', [])

        try:
            role = Role.objects.get(role=role_name)
        except Role.DoesNotExist:
            return Response({"error": f"Role '{role_name}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        users = []
        for email in email_addresses:
            try:
                user = CustomUser.objects.get(email=email)

                if RoleManagement.objects.filter(event_id=event, user_id=user).exists():
                    return Response({"message": f"Emails is already registered"}, status=status.HTTP_201_CREATED)

            except CustomUser.DoesNotExist:
                user = CustomUser.objects.create_user(email=email, username=email)
                
                subject = 'Added to a role for an event'
                message = f'You have been added for role: {role_name} for the event: {event.name}'
                from_email = 'rishabhagarwal9935@gmail.com'
                rec_list = [email,]
                send_mail(subject, message, from_email, rec_list)
                
            users.append(user)

        role_managements = []
        for user in users:
            role_management, created = RoleManagement.objects.get_or_create(event_id=event, user_id=user, role_id=role)
            role_managements.append(role_management)

        return Response({"message": f"Emails added to role '{role_name}' successfully."}, status=status.HTTP_201_CREATED)

    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)

        host_role = Role.objects.get(role='host')
        organiser_role = Role.objects.get(role='organiser')
        volunteer_role = Role.objects.get(role='volunteer')
        donor_role = Role.objects.get(role='donor')

        host = RoleManagement.objects.filter(event_id=event, role_id=host_role).values_list('user_id__username', flat=True)
        organisers = RoleManagement.objects.filter(event_id=event, role_id=organiser_role).values_list('user_id__username', flat=True)
        volunteer = RoleManagement.objects.filter(event_id=event, role_id=volunteer_role).values_list('user_id__username', flat=True)
        donor = RoleManagement.objects.filter(event_id=event, role_id=donor_role).values_list('user_id__username', flat=True)

        response_data = {
            'host': list(host),
            'organisers': list(organisers),
            'volunteers': list(volunteer),
            'donors': list(donor)
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request, event_id, username):
        event = get_object_or_404(Event, id=event_id)
        if not username:
            return Response({"error": "Username is required in the request body."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": f"User '{username}' does not exist."}, status=status.HTTP_404_NOT_FOUND)

        try:
            host_role = Role.objects.get(role='host')
            organiser_role = Role.objects.get(role='organiser')
            volunteer_role = Role.objects.get(role='volunteer')
            donor_role = Role.objects.get(role='donor')
            # organiser_role = Role.objects.get(role='organiser')
            # volunteer_role = Role.objects.get(role='volunteer')
        except Role.DoesNotExist:
            return Response({"error": "One or both of the roles 'organiser' and 'volunteer' do not exist."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            role_management = RoleManagement.objects.get(event_id=event, user_id=user, role_id__in=[organiser_role, volunteer_role, host_role, donor_role])
            role_management.delete()
            return Response({"message": f"User '{username}' role for the event deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except RoleManagement.DoesNotExist:
            return Response({"error": f"User '{username}' is not an organiser or volunteer for this event."}, status=status.HTTP_404_NOT_FOUND)



class InviteAttendees(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, event_id):
        email_list = request.data.get('emailList', [])
        message = request.data.get('message', '')
        event = get_object_or_404(Event, id=event_id)

        if event.is_private:
            if not IsHost().has_permission(request=request, event=event, view=self) and not IsOrganiser().has_permission(request=request, event=event, view=self):
                return Response({"error": "You don't have permission to send invites for this event."}, status=status.HTTP_403_FORBIDDEN)

            for email in email_list:
                frontend_url = f'http://localhost:3000/choices/{event_id}/{email}'
                invitation_message = f"{message}\n\nPlease respond to the invitation here: {frontend_url}"
                send_mail(
                    subject='Invitation to Event',
                    message=invitation_message, 
                    from_email='rishabhagarwal9935@gmail.com',
                    recipient_list=[email],
                    fail_silently=False,
                )
                try:
                    user = CustomUser.objects.get(email=email)
                except:
                    user = CustomUser.objects.create_user(username=email, email=email, password='1234')
                    
                
                if user:
                    RoleManagement.objects.get_or_create(event_id=event, user_id=user, role_id=Role.objects.get(role = 'attendees'))
                else:
                    Response({"message" : "User not exist"})
            return Response({"message": "Invitations sent and attendees added successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error" : "This is not a private event"}, status=status.HTTP_400_BAD_REQUEST)
    

class HandleAttendeeResponse(APIView):
    def post(self, request, event_id, email):
        event = get_object_or_404(Event, id=event_id)
        response = request.data.get('response')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        role_name = 'attending' if response == 'accept' else 'not_attending'
        if role_name == 'attending':
            RoleManagement.objects.create(event_id=event, user_id=user, role_id=Role.objects.get(role = role_name))
            RoleManagement.objects.filter(event_id=event, user_id=user, role_id=Role.objects.get(role = 'not_attending')).delete()
        else:
            RoleManagement.objects.create(event_id=event, user_id=user, role_id=Role.objects.get(role = role_name))
            RoleManagement.objects.filter(event_id=event, user_id=user, role_id=Role.objects.get(role = 'attending')).delete()
        
        if response == 'accept':
            return Response({"message": "Invitation accepted."}, status=status.HTTP_200_OK)
        elif response == 'reject':
            return Response({"message": "Invitation rejected."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid response."}, status=status.HTTP_400_BAD_REQUEST)


class GetCurrentUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    

class RoleAPIView(APIView):  
    def get(self, request, event_id):
        print('role here')
        
        try:
            event = Event.objects.get(id = event_id)
        except Event.DoesNotExist:
            return Response('Invalid event id', status=status.HTTP_404_NOT_FOUND)
        
        host = IsHost()
        organiser = IsOrganiser()
        volunteer = IsVolunteer()
        attendees = IsAttendee()

        my_role = 'None'
        
        if volunteer.has_permission(request=request, event=event, view=self):
            my_role = 'Volunteer'

        if organiser.has_permission(request=request, event=event, view=self):
            my_role = 'Organiser'

        if host.has_permission(request=request, event=event, view=self):
            my_role = 'Host'

        if attendees.has_permission(request=request, event=event, view=self):
            my_role = 'Attendees'

        # return Response({'role' : my_role })
        roles_available = Role.ROLE_CHOICES

        roles_available = [ role[0] for role in roles_available if role[0] not in ['host', 'attendees', 'attending', 'not_attending'] ]
        
        
        return Response({'role' : my_role, 'roles_available' : roles_available })
    

class AddDonorAPIView(APIView):
    def post(self, request):
        serializer = DonorSerializer(data=request.data)
        if serializer.is_valid():
            donor_name = serializer.validated_data['donor_name']
            email = serializer.validated_data['email']


            donor, created = Donor.objects.get_or_create(email=email, defaults={'donor_name': donor_name})

            user = request.user
            DonorManagement.objects.create(donor_id=donor, user_id=user)

            try:
                user = CustomUser.objects.get(email=email)
            except:
                user = CustomUser.objects.create_user(username=email, email=email, password='1234')
            send_mail(
                'Thank You for Your Contribution',
                'You have been added as a donor. Thank you for your support!, Your username is your email and password is 1234. Please login and reset your password',
                'rishabhagarwal9935@gmail.com',
                [email],
                fail_silently=True,
            )

            return Response({'message': 'Donor added successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DonorListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        donor_management = DonorManagement.objects.filter(user_id = request.user)
        donor_ids = donor_management.values_list('donor_id', flat=True)
        donors = Donor.objects.filter(id__in = donor_ids)
        serializer = DonorSerializer(donors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request):
        email = request.data.get('email')
        print(email)
        if email:
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found with the provided email'}, status=status.HTTP_404_NOT_FOUND)

            if user.rolemanagement_set.filter(role_id__role='donor').exists():
                return Response({'error': 'User is already a donor'}, status=status.HTTP_400_BAD_REQUEST)

            event_id = request.data.get('eventId')
            event = Event.objects.get(pk=event_id)
            role_donor = Role.objects.get(role='donor')
            RoleManagement.objects.create(event_id=event, user_id=user, role_id=role_donor)

            subject = 'Invitation'
            message = f'You have been invited for {event.name} as a donor. Thank you for your support!'
            email_from = 'rishabhagarwal9935@gmail.com'
            rec_list = [email,]
            send_mail(subject, message, email_from, rec_list)

            return Response({'message': 'User added as donor successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)


class SilentAuctionView(APIView):
    def get(self, request,event_id):
            event = Event.objects.get(pk=event_id)
            auctions = Auction.objects.get(user_id=request.user,event_id=event)
            serializer = SilentAuctionSerializer(auctions)
            return Response(serializer.data)
    
    def post(self, request, event_id):
            user_id = request.user
            event = Event.objects.get(pk=event_id)

            # bid_data = {
            #     'user_id': user_id,
            #     'event_id': event_id,
            #     'bid': request.data.get('bid')
            # }
            # print(bid_data)

            serializer = SilentAuctionSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save(user_id=user_id, event_id=event)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
class HighestBidView(APIView):
    def get(self, request, event_id):
        try:
            highest_bid = Auction.objects.filter(event_id=event_id).order_by('-bid').select_related('user_id').first()
            if highest_bid:
                serializer = SilentAuctionSerializer(highest_bid)
                user_name = highest_bid.user_id.username
                serialized_data = serializer.data
                serialized_data['user_name'] = user_name
                return Response(serialized_data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No bids for this event yet'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class RandomRaffleView(APIView):
    def get(self, request, event_id):
        try:
            attendees = RoleManagement.objects.filter(event_id=event_id, role_id__role='attendees')
            
            if attendees.exists():
                random_attendee = random.choice(attendees)
                user_info = {
                    'user_id': random_attendee.user_id.id,
                    'user_name': random_attendee.user_id.username,
                    'user_email': random_attendee.user_id.email
                }

                return JsonResponse(user_info, status=200)
            else:
                return JsonResponse({'message': 'No attendees found for the event'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        








  # for event in events:
        #     if event.is_private:
        #         if (IsHost().has_permission(request=request,event=event ,view=self) 
        #             or IsOrganiser().has_permission(request=request,event=event, view=self) 
        #             or IsVolunteer().has_permission(request=request,event=event, view=self) 
        #             or IsAttendee().has_permission(request=request,event=event, view=self)):
        #             data += [{
        #             'id': event.id,
        #             'name': event.name,
        #             'date': event.date,
        #             'location': event.location,
        #             'description': event.description,
        #             'photo' : str(event.photo.url if event.photo else None)}]
        #     else:
        #         data += [{
        #             'id': event.id,
        #             'name': event.name,
        #             'date': event.date,
        #             'location': event.location,
        #             'description': event.description,
        #             'photo' : str(event.photo.url if event.photo else None)}]