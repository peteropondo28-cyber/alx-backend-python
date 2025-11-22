import logging
import time
from datetime import datetime
from django.http import HttpResponseForbidden

# -------------------------------------------------------------------
# 1. Request Logging Middleware
# -------------------------------------------------------------------

logger = logging.getLogger("request_logger")
handler = logging.FileHandler("requests.log")
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    """
    Logs every user request with date, user, and path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else "Anonymous"

        log_msg = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_msg)

        return self.get_response(request)


# -------------------------------------------------------------------
# 2. Restrict Access By Time Middleware
# -------------------------------------------------------------------

class RestrictAccessByTimeMiddleware:
    """
    Restricts chat access outside 6 AM - 9 PM.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        hour = datetime.now().hour

        if hour >= 21 or hour < 6:
            return HttpResponseForbidden(
                "The messaging service is unavailable at this time. "
                "Allowed hours are 6:00 AM to 9:00 PM."
            )

        return self.get_response(request)


# -------------------------------------------------------------------
# 3. Offensive Language / Message Flood Protection Middleware
# -------------------------------------------------------------------

class OffensiveLanguageMiddleware:
    """
    Limits POST requests from each IP to 5 per minute.
    Prevents message spam or offensive flooding.
    """

    RATE_LIMIT = 5
    TIME_WINDOW = 60
    ip_requests = {}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.method == "POST":
            ip = request.META.get("REMOTE_ADDR", "unknown")
            now = time.time()

            if ip not in self.ip_requests:
                self.ip_requests[ip] = []

            # Keep timestamps from past minute only
            self.ip_requests[ip] = [
                t for t in self.ip_requests[ip] if now - t < self.TIME_WINDOW
            ]

            if len(self.ip_requests[ip]) >= self.RATE_LIMIT:
                return HttpResponseForbidden(
                    "Message rate limit exceeded. Only 5 messages per minute allowed."
                )

            self.ip_requests[ip].append(now)

        return self.get_response(request)


# -------------------------------------------------------------------
# 4. Role Permission Middleware
# -------------------------------------------------------------------

class RolePermissionMiddleware:
    """
    Only allows users with admin or moderator roles
    to access protected routes.
    """

    ALLOWED_ROLES = ["admin", "moderator"]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        user = request.user

        if not user.is_authenticated:
            return self.get_response(request)

        role = getattr(user, "role", "user")

        if role not in self.ALLOWED_ROLES:
            return HttpResponseForbidden(
                "You do not have permission to perform this action."
            )

        return self.get_response(request)
