import logging
from datetime import datetime

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
