from rest_framework import permissions


class UsernamePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        username = request.user.username

        if username != "badaong":
            return False
        else:
            return True
