import json
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import authenticate
from event_management.models import CustomUser, AccessAttempt 
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError


class AccessTrackingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == '/api/login/':
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            password = data.get('password')

            user = CustomUser.objects.get(username=username)
            auth_user = authenticate(username=username, password=password)
                
            attempt, is_created = AccessAttempt.objects.get_or_create(user=user, logout_time=None, defaults={ 
                'first_attempt_time': timezone.now()
            })
            
            if attempt.failed_logins == 0 and attempt.login_time is None:
                attempt.first_attempt_time = timezone.now()
            
            if auth_user:
                attempt.login_time = timezone.now()
                attempt.failed_logins = 0 
            else:
                attempt.failed_logins += 1
                
            attempt.save()

    # def process_response(self, request, response):
    #     print(request.user)
    #     if request.path == '/api/logout/':
    #         token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
    #         print(token)
    #         try:
    #             access_token = AccessToken(token)
    #             access_token.verify()
    #             payload = access_token.payload
    #         except TokenError as e:
    #             return response

    #         user = CustomUser.objects.get(pk=payload['user_id'])

    #         attempt = AccessAttempt.objects.get(user=user.id, logout_time=None)
    #         attempt.logout_time = timezone.now()
    #         attempt.save()

    #     return response

    def process_response(self, request, response):
        if request.path == '/api/logout/':
            print("1")
            print(request)
            if request.user.is_authenticated:
                print("2")
                user = request.user
                print("3")
                print(user)
                try:
                    attempt = AccessAttempt.objects.get(user=user, logout_time=None)
                    attempt.logout_time = timezone.now()
                    attempt.save()
                except AccessAttempt.DoesNotExist:
                    print("Not logged In")

        return response




















































# import json
# from django.utils import timezone
# from django.utils.deprecation import MiddlewareMixin
# from django.contrib.auth import authenticate
# from event_management.models import CustomUser, AccessAttempt  # Adjust this if your user model is different
# from rest_framework_simplejwt.tokens import AccessToken
# from rest_framework_simplejwt.exceptions import TokenError


# class AccessTrackingMiddleware(MiddlewareMixin):

#     def process_request(self, request):
#         if request.path == '/api/login/':
#             data = json.loads(request.body.decode('utf-8'))
#             username = data.get('username')
#             password = data.get('password')

#             user = CustomUser.objects.get(username=username)
#             auth_user = authenticate(username=username, password=password)
                
#             attempt, is_created = AccessAttempt.objects.get_or_create(user=user, logout_time=None, defaults={ 
#                 'first_attempt_time': timezone.now()
#             })
            
#             if attempt.failed_logins == 0 and attempt.login_time is None:
#                 attempt.first_attempt_time = timezone.now()
            
#             if auth_user:
#                 attempt.login_time = timezone.now()
#             else:
#                 attempt.failed_logins += 1
                
#             attempt.save()

#     def process_response(self, request, response):
#         if request.path == '/api/logout/':
#             token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
#             print(token)
#             try:
#                 access_token = AccessToken(token)
#                 access_token.verify()
#                 payload = access_token.payload
#             except TokenError as e:
#                 return response

#             user = CustomUser.objects.get(pk=payload['user_id'])

#             attempt = AccessAttempt.objects.get(user=user.id, logout_time=None)
#             attempt.logout_time = timezone.now()
#             attempt.save()

#         return response











# # # middleware.py

# # from datetime import datetime
# # from django.utils.timezone import now
# # from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed
# # from .models import AccessAttempt, CustomUser
# import json
# from django.utils import timezone
# from django.utils.deprecation import MiddlewareMixin
# from django.contrib.auth import authenticate
# from event_management.models import CustomUser, AccessAttempt
# from rest_framework_simplejwt.tokens import AccessToken
# from rest_framework_simplejwt.exceptions import TokenError

# class AccessTrackingMiddleware(MiddlewareMixin):
#     def process_request(self,request):
        
#         if request.path == '/api/login/':
#             print('in login att')
#             data = json.loads(request.body.decode('utf-8'))
#             username = data.get('username')
#             password = data.get('password')

#             print('username', username)
#             print('req.user', request.user)
#             user = CustomUser.objects.get(username=username)
#             auth_user = authenticate(username=username, password=password)
                
#             attempt, is_created = AccessAttempt.objects.get_or_create(user=user, logout_time=None, defaults={ 
#                 'first_attempt_time':timezone.now()
#             })
            
#             if attempt.failed_logins == 0 and attempt.login_time == None:
#                 attempt.first_attempt_time == timezone.now()
            
#             if auth_user:
#                 attempt.login_time = timezone.now()
                
#             else:
#                 attempt.failed_logins += 1
                
#             attempt.save()
            
#         if request.path == '/api/logout/':
#             token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
#             print(token)
            
#             try:
#                 access_token = AccessToken(token)
#                 access_token.verify()

#                 payload = access_token.payload
#                 print('payload:', payload)
#             except TokenError as e:
#                 print(e)
                
#             user = CustomUser.objects.get(pk=payload['user_id'])
            
#             print('from else', user)
            
#             attempt = AccessAttempt.objects.get(user=user.id, logout_time=None)
            
#             attempt.logout_time = timezone.now()
            
#             attempt.save()

















