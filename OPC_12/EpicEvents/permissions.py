from rest_framework.permissions import BasePermission
from datetime import date


class HasClientPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Support'):
            return request.method == 'GET'
        elif request.user.groups.filter(name='Sales'):
            return request.method in ['GET', 'POST', 'PUT']
        elif request.user.is_staff or request.user.is_superuser:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Support'):
            return request.method == 'GET'
        elif request.user.groups.filter(name='Sales'):
            if request.user == obj.SalesContact:
                return request.method in ['GET', 'PUT']
        elif request.user.is_staff or request.user.is_superuser:
            return True


class HasContractPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Sales'):
            return request.method in ['GET', 'POST', 'PUT']
        elif request.user.is_staff or request.user.is_superuser:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Sales'):
            if request.user == obj.SalesContact:
                return request.method in ['GET', 'PUT']
        elif request.user.is_staff or request.user.is_superuser:
            return True


class HasEventPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Support'):
            return request.method in ['GET', 'PUT']
        elif request.user.groups.filter(name='Sales'):
            return request.method in ['GET', 'POST']
        elif request.user.is_staff or request.user.is_superuser:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Support'):
            if request.user == obj.SupportContact:
                if obj.EventDate > date.today():
                    return request.method in ['GET', 'PUT']
                elif obj.EventDate <= date.today():
                    return request.method == 'GET'
        elif request.user.is_staff or request.user.is_superuser:
            return True


class HasUserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff or request.user.is_superuser:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
