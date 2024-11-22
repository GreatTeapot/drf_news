from rest_framework import serializers
from users.models.profile import Profile


class ProfileShortSerializer(serializers.ModelSerializer):
    """
    Nested profile serializer.
    """

    class Meta:
        model = Profile
        fields = ('photo',)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Nested profile update serializer.
    """

    class Meta:
        model = Profile
        fields = ('photo',)
