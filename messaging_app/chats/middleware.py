import logging
import time
from datetime import datetime
from collections import defaultdict
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
        
        # Restrict access to the chat between 9 PM and 6 PM
        if current_hour < 9 or current_hour >= 18:
            # If the request is outside of the allowed hours, deny access
            return JsonResponse(
                {"error": "Access to the messaging system is restricted between 9 PM and 6 PM."},
                status=403
            )

        # Otherwise, allow the request to proceed
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """
    Middleware that limits the number of chat messages a user can send within a time window.
    Tracks message count per IP address and enforces a limit of 5 messages per minute.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track message counts per IP address
        self.message_counts = defaultdict(list)  # IP -> list of timestamps

    def __call__(self, request):
        # Only track POST requests to the messaging endpoint
        if request.method == "POST" and request.path.startswith('/api/messages/'):
            ip_address = request.META.get('REMOTE_ADDR')  # Get user's IP address
            current_time = time.time()  # Current time in seconds

            # Clean up old timestamps older than 1 minute (60 seconds)
            self.message_counts[ip_address] = [
                timestamp for timestamp in self.message_counts[ip_address] if current_time - timestamp < 60
            ]

            # Check if the user has exceeded the limit (5 messages per minute)
            if len(self.message_counts[ip_address]) >= 5:
                return JsonResponse(
                    {"error": "You have exceeded the message limit of 5 messages per minute."},
                    status=403
                )

            # If the limit has not been exceeded, log the new message timestamp
            self.message_counts[ip_address].append(current_time)

        # Proceed to the next middleware or view
        response = self.get_response(request)
        return response
