from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsCollegeAuthority(BasePermission):
    """
    GET allowed for everyone
    POST/PUT/PATCH/DELETE only for top authority users
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff
