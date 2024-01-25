from rest_framework import permissions


class GroupPermission(permissions.BasePermission):

    # 그룹이 없을 경우에 True 반환
    def has_permission(self, request, view):
        groups = request.user.groups.all()

        if not groups:
            return True
        else:
            return False