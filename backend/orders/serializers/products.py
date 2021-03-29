from rest_framework import serializers

from orders.models import SavedProduct


class SavedProductSerializer(serializers.ModelSerializer):
    """
    Serialize SavedProduct
    """

    class Meta:
        model = SavedProduct
        fields = (
            "id",
            "product_id",
            "title",
            "width",
            "height",
            "length",
            "weight",
            "retail_price",
        )
