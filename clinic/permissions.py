from rest_framework import permissions
from .models import UserProfile


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_profile.role.name == 'Admin':
            return True


class IsOperator(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_profile.role.name == 'operator':
            return True


class IsDoctor(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_profile.role.name == 'doctor':
            return True
