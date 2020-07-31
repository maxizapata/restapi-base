from rest_framework.permissions import BasePermission


class MobileIsVerify(BasePermission):
    """
    Allow access only if verify number database field is True
    """

    def has_permission(self, request, view):
        return request.user.verified_mobile
