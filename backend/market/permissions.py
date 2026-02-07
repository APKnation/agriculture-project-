from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the object.
        return obj.farmer == request.user

class IsFarmer(permissions.BasePermission):
    """
    Custom permission to only allow farmers to access the resource.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'farmer'

class IsOfficer(permissions.BasePermission):
    """
    Custom permission to only allow market officers to access the resource.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'officer'

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins to access the resource.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsFarmerOrOfficer(permissions.BasePermission):
    """
    Custom permission to allow farmers and officers to access the resource.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role in ['farmer', 'officer'])

class IsOfficerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow officers and admins to access the resource.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role in ['officer', 'admin'])

class CanAccessAnalytics(permissions.BasePermission):
    """
    Custom permission to allow officers and admins to access analytics.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role in ['officer', 'admin'])

class CanManageUsers(permissions.BasePermission):
    """
    Custom permission to only allow admins to manage users.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role == 'admin')
