from rest_framework.throttling import UserRateThrottle

class LoginRateThrottle(UserRateThrottle):
    """
    Custom throttle for login attempts.
    Limits number of login requests per user/IP.
    """
    rate = "1/min"  