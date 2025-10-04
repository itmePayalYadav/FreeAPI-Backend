from rest_framework.permissions import BasePermission

# ----------------------------
# Admin Only (superuser/staff)
# ----------------------------
class IsAdminUser(BasePermission):
    """
    Allows access only to superuser or staff users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))

# ----------------------------
# Premium Users Only
# ----------------------------
class IsPremiumUser(BasePermission):
    """Allows access only to premium users."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_premium)

# ----------------------------
# Free or Premium Users
# ----------------------------
class IsAuthenticatedUser(BasePermission):
    """Allows access to any authenticated user (free or premium)."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
