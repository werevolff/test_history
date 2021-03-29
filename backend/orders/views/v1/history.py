from django_filters import rest_framework as filters
from rest_framework import pagination, viewsets, mixins

from orders.models import Order, Event
from orders.serializers.history import EventSerializer


class EventFilterSet(filters.FilterSet):
    """
    Event FilterSet
    """

    class Meta:
        model = Event
        fields = ("order",)

    order = filters.ModelChoiceFilter(name="order", queryset=Order.objects.all())


class EventViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Event ViewSet
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = pagination.LimitOffsetPagination
