from django.contrib.auth import get_user_model

from rest_framework import mixins, viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

from huscy.users import models, serializer


class ReadOnlyForNonAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.method in SAFE_METHODS


class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = get_user_model().objects.order_by('last_name', 'first_name')
    serializer_class = serializer.UserSerializer
    permission_classes = (IsAuthenticated, ReadOnlyForNonAdmin)


class UserProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = serializer.UserProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        profile, _created = models.UserProfile.objects.get_or_create(user=self.request.user)
        return profile
