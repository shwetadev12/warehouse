from rest_framework.permissions import BasePermission


class ProfileTypePermission(BasePermission):
    profile_type = None

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.profile_type == self.profile_type
        )


class OwnerPermission(ProfileTypePermission):
    profile_type = 'warehouses_owner'


class ManagerPermission(ProfileTypePermission):
    profile_type = 'warehouses_manager'


class CompanyPermission(ProfileTypePermission):
    profile_type = 'company_owner'
