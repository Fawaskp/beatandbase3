from django.shortcuts import redirect
from admin_home.views import admin_login
from django.urls import reverse

class LogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if not request.user.is_authenticated:
            # If the user is not authenticated, redirect them to a different page
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            response['Location'] = reverse('login') # change 'login' to your desired redirect url
        
        return redirect(admin_login)