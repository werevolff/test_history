import factory
from pytest_factoryboy import register


@register
class OrderFactory(factory.django.DjangoModelFactory):
    """
    Order Factory
    """

    class Meta:
        model = "orders.Order"


@register
class OrderItemFactory(factory.django.DjangoModelFactory):
    """
    OrderItem Factory
    """

    class Meta:
        model = "orders.OrderItem"
        django_get_or_create = ("saved_product",)

    order = factory.SubFactory(OrderFactory)
    saved_product = factory.SubFactory("orders.tests.factories.products.SavedProductFactory")
