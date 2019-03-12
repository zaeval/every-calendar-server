from rest_framework import permissions
class HasAPIAccess(permissions.BasePermission):
    message = 'Invalid or missing API Key.'

    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_API_KEY', '')
        pass
        # return APIKey.objects.filter(key=api_key).exists()
