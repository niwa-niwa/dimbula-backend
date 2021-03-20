from rest_framework import serializers

from person.models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'id',
            'firebase_id',
            'name',
            'email',
            'email_verified',
            'photo_url',
            'provider_id',
            'is_admin',
            'is_active',
        ]
