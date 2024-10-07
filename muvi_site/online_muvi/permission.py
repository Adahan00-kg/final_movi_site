from rest_framework import permissions


class CheckMovie(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.status == 'pro' :
            return True
        elif request.user.status == 'simple':
            if obj.status_movie == 'pro':
                return False
            elif obj.status_movie == 'silver':
                return True


