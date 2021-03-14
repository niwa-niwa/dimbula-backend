from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email_verified',
            'photo_url',
            'provider_id',
            'is_admin',
            'updated_at',
        ]
