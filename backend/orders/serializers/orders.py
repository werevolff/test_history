from rest_framework import serializers

from orders.models import Order, OrderItem
from orders.serializers.products import SavedProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serialize OrderItem
    """

    class Meta:
        model = OrderItem
        fields = ("id", "saved_product_id", "saved_product", "product")

    saved_product = SavedProductSerializer()


class OrderSerializer(serializers.ModelSerializer):
    """
    Serialize Order
    """

    class Meta:
        model = Order
        fields = ("id", "created", "state", "order_items")

    order_items = OrderItemSerializer(many=True)
