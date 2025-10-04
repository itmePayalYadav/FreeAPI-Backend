from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from django.db.models import Q  
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import UserRateThrottle
from core.throttles import LoginRateThrottle
from .serializers import UserRegisterSerializer, UserSerializer
from core.utils import api_success, api_error
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.models import User

class RegisterUserView(APIView):
    """
    User registration endpoint.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return api_success(
                data=UserSerializer(user).data,
                message="User registered successfully",
                status_code=status.HTTP_201_CREATED
            )
        return api_error(
            errors=serializer.errors,
            message="User registration failed",
            status_code=status.HTTP_400_BAD_REQUEST
        )

class LoginUserView(APIView):
    """
    User login endpoint with JWT token generation.
    """
    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]

    def post(self, request):
        identifier = request.data.get("identifier")
        password = request.data.get("password")
    

        if not identifier or not password:
            return api_error(
                errors={"detail": "Username/ Email and password are required."},
                message="User login failed",
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            user_obj = User.objects.get(Q(username=identifier) | Q(email__iexact=identifier))
        except User.DoesNotExist:
            return api_error(
                errors={"detail": "Invalid username/email or password"},
                message="Login failed",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        user = authenticate(username=user_obj.username, password=password)
        
        if not user:
            return api_error(
                errors={"detail": "Invalid username/email or password"},
                message="Login failed",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return api_success(
            data={
                "user": UserSerializer(user).data,
                "tokens": {
                    "access": access_token,
                    "refresh": refresh_token
                }
            },
            message="User login successful",
            status_code=status.HTTP_200_OK
        )

class UserProfileView(APIView):
    """
    Protected endpoint: returns current user's profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serialized_user = UserSerializer(user).data 

        print(serialized_user)  

        return api_success(
            data={"user": serialized_user},
            message="User profile retrieved successfully"
        )

class LogoutUserView(APIView):
    """
    Logout user by blacklisting refresh token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return api_error(
                errors={"detail": "Refresh token is required"},
                message="Logout failed",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return api_success(
                data={},
                message="User logged out successfully",
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            return api_error(
                errors={"detail": str(e)},
                message="Logout failed",
                status_code=status.HTTP_400_BAD_REQUEST
            )
            