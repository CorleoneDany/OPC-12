from rest_framework.permissions import BasePermission, SAFE_METHODS


def HasClientPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Support'):
            return request.method in SAFE_METHODS
        elif request.user.groups.filter(name='Sales'):
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Support'):
            return request.method in SAFE_METHODS
        elif request.user.groups.filter(name='Sales'):
            if request.user == obj.sales_contact:
                return True
        elif request.user.is_staff:
            return True


def HasContractPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Sales'):
            if request.user == obj.sales_contact:
                return True
        elif request.user.is_staff:
            return True


def HasEventPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Support'):
            if request.user == obj.sales_contact:
                return True
        elif request.user.is_staff:
            return True
