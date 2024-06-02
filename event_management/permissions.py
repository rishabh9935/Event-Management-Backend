from rest_framework import permissions # type: ignore
from .models import RoleManagement

class IsOrganiser(permissions.BasePermission):
    def has_permission(self, request, event, view):
        if not request.user.is_authenticated:
            return False
        
        event_id = view.kwargs.get('event_id')
        if event_id:
            return request.user.rolemanagement_set.filter(event_id=event_id, user_id = request.user.id, role_id__role='organiser').exists()
        elif event.id:
            return request.user.rolemanagement_set.filter(event_id=event.id, user_id=request.user.id, role_id__role='organiser').exists()
        
        return False
        

class IsHost(permissions.BasePermission):
    def has_permission(self, request, event, view):
        if not request.user.is_authenticated:
            print("1")
            return False
        
        event_id = view.kwargs.get('event_id')
        print("2")
        if event_id:
            print("3")
            return request.user.rolemanagement_set.filter(event_id=event_id, user_id = request.user.id, role_id__role='host').exists()
        elif event.id:
            print("4")
            return request.user.rolemanagement_set.filter(event_id=event.id, user_id=request.user.id, role_id__role='host').exists()
        
        print("5")
        return False

class IsVolunteer(permissions.BasePermission):
    def has_permission(self, request, event, view):
        if not request.user.is_authenticated:
            return False
        
        event_id = view.kwargs.get('event_id')
        if event_id:
            return request.user.rolemanagement_set.filter(event_id=event_id, user_id = request.user.id, role_id__role='volunteer').exists()
        elif event.id:
            return request.user.rolemanagement_set.filter(event_id=event.id, user_id=request.user.id, role_id__role='volunteer').exists()
        
        return False
    
class IsAttendee(permissions.BasePermission):
    def has_permission(self, request, event, view):
        if not request.user.is_authenticated:
            return False
        
        event_id = view.kwargs.get('event_id')
        if event_id:
            return request.user.rolemanagement_set.filter(event_id=event_id, user_id = request.user.id, role_id__role='attendees').exists()
        elif event.id:
            return request.user.rolemanagement_set.filter(event_id=event.id, user_id=request.user.id, role_id__role='attendees').exists()
        
        return False

class isEventPart(permissions.BasePermission):
    def has_permission(self, request, event, view):
        user = request.user
        if not request.user.is_authenticated:
            return False
        try:
            isPresent = RoleManagement.objects.filter(user_id=user, event_id=event)
            if(len(isPresent)):
                return True
            else:
                return False
        except RoleManagement.DoesNotExist:
            return False


# from rest_framework import permissions
# from .models import Event, Role, RoleManagement

# class IsHost(permissions.BasePermission):

#     def has_permission(self, request, view):
#         if not request.user.is_authenticated:
#             return False
        
#         event_id = view.kwargs['event_id']
#         if event_id:
#             event = Event.objects.get(pk=event_id)
#             host_role = Role.objects.get(role='host')
#             if RoleManagement.objects.filter(event_id=event, user_id=request.user, role_id=host_role).exists():
#                 # print('auth pass')
#                 return True
            
#             return False
        
#         return False

# class IsOrganiser(permissions.BasePermission):

#     def has_permission(self, request, view):
        
#         if not request.user.is_authenticated:
#             return False
        
#         event_id = view.kwargs['event_id']
#         if event_id:
#             event = Event.objects.get(pk=event_id)
#             host_role = Role.objects.get(role='organiser')
#             if RoleManagement.objects.filter(event_id=event, user_id=request.user, role_id=host_role).exists():
#                 return True
            
#             return False
        
#         return False

# class IsVolunteer(permissions.BasePermission):

#     def has_permission(self, request, view):
        
#         if not request.user.is_authenticated:
#             return False
        
#         event_id = view.kwargs['event_id']
#         if event_id:
#             event = Event.objects.get(pk=event_id)
#             host_role = Role.objects.get(role='Volunteer')
#             if RoleManagement.objects.filter(event_id=event, user_id=request.user, role_id=host_role).exists():
#                 print('AUTH VOL PASS')
#                 return True
            
#             return False
        
#         return False
    

# class IsAttendee(permissions.BasePermission):

#     def has_permission(self, request, view):
        
#         if not request.user.is_authenticated:
#             return False
        
#         event_id = view.kwargs['event_id']
#         if event_id:
#             event = Event.objects.get(pk=event_id)
#             host_role = Role.objects.get(role='Attendees')
#             if RoleManagement.objects.filter(event_id=event, user_id=request.user, role_id=host_role).exists():
#                 print('AUTH VOL PASS')
#                 return True
            
#             return False
        
#         return False
    
# class IsHostIsAttendeeIsOrganiserIsVolunteer(permissions.BasePermission):
#     IsVolunteer()


