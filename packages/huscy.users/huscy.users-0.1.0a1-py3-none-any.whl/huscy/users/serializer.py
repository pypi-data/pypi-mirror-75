from django.contrib.auth import get_user_model

from rest_framework import serializers

from huscy.users.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source='get_full_name')

    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'full_name',
            'id',
            'last_name',
            'password',
            'username',
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'id',
            'prefered_language',
            'user',
        )
        read_only_fields = (
            'user',
        )
