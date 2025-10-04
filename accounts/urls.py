from django.urls import path
from .views import RegisterUserView, LoginUserView, UserProfileView, LogoutUserView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    # Protected
    path("profile/", UserProfileView.as_view(), name="profile"),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]
