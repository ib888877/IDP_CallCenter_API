from rest_framework.permissions import BasePermission
from django.conf import settings

class HasAPIKey(BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get('X-API-KEY')
        return token is not None and token == settings.API_TOKEN
