from rest_framework import permissions


class ReviewEditPermission(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if (request.user and request.user.is_staff) or request.user.is_admin:
            return True

        if request.method not in permissions.SAFE_METHODS:
            return request.user == obj.review_user

        return True

class StaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        else:
            return request.user and request.user.is_authenticated and request.user.is_staff