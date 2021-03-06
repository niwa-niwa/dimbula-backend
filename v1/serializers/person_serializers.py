from rest_framework import serializers

from person.models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'id',
            'name',
            'email',
            'photo_url',
            'created_at',
            'updated_at',
            'last_login',
            'is_superuser',
        ]
