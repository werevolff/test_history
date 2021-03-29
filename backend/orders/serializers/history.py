from django.contrib.auth import get_user_model
from rest_framework import serializers

from orders.models import Event

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """

    class Meta:
        model = User
        fields = ("id", "username", "email", "full_name")

    full_name = serializers.CharField(source="get_full_name")


class EventSerializer(serializers.ModelSerializer):
    """
    Serialize event
    """

    class Meta:
        model = Event
        fields = ("id", "event_type", "subtype", "user", "difference")

    user = UserSerializer
