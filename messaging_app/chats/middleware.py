import logging
from datetime import datetime
from django.http import JsonResponse
from django.utils import timezone

# Create a logger instance
logger = logging.getLogger('django')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('user_requests.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class RequestLoggingMiddleware:
    """
    Middleware that logs each user's request with timestamp, user, and request path.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the user (handle anonymous users)
        user = request.user if request.user.is_authenticated else 'Anonymous'
        
        # Log the information
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        
        # Proceed to the next middleware or view
        response = self.get_response(request)
        
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the messaging system outside 9 PM and 6 PM.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the current time in the server's local timezone
        current_hour = timezone.localtime(timezone.now()).hour
        
        # Restrict access to the chat between 6 AM and 9 PM
        if current_hour < 9 or current_hour >= 18:
            # If the request is outside of the allowed hours, deny access
            return JsonResponse(
                {"error": "Access to the messaging system is restricted between 9 PM and 6 PM."},
                status=403
            )

        # Log the request information (after time check)
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        
        # Otherwise, allow the request to proceed
        response = self.get_response(request)
        return response
