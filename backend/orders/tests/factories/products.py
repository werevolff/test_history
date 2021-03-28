import factory
from factory.fuzzy import FuzzyText, FuzzyDecimal
from pytest_factoryboy import register


@register
class ProductFactory(factory.django.DjangoModelFactory):
    """
    Product Factory
    """

    class Meta:
        model = "orders.Product"

    title = FuzzyText()


@register
class SavedProductFactory(factory.django.DjangoModelFactory):
    """
    Stock items factory
    """

    class Meta:
        model = "orders.SavedProduct"

    product = factory.SubFactory(ProductFactory)
    width = FuzzyDecimal(10, 100)
    height = FuzzyDecimal(10, 100)
    length = FuzzyDecimal(10, 100)
    weight = FuzzyDecimal(10, 100)
    retail_price = FuzzyDecimal(100, 500)
