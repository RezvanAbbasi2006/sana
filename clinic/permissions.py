from rest_framework import permissions
from rest_framework.authtoken.admin import User

from .models import UserProfile


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = User.objects.get(id=request.GET['user_id'])
        if user.user_profile.role.name == 'Admin':
            return True


class IsOperator(permissions.BasePermission):

    def has_permission(self, request, view):
        user = User.objects.get(id=request.GET['user_id'])
        if user.user_profile.role.name == 'operator':
            return True


class IsDoctor(permissions.BasePermission):

    def has_permission(self, request, view):
        user = User.objects.get(id=request.GET['user_id'])
        if user.user_profile.role.name == 'doctor':
            return True
