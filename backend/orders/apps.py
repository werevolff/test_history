from django.apps import AppConfig
from django.db.models.signals import post_save


class OrdersConfig(AppConfig):
    name = "orders"

    def ready(self):
        # Yes, I know this is a bad decision. But, as part of the test task,
        # I decided to ignore this.
        from orders.signals import post_save_store_event
        super().ready()
        models_running_store_event = ("Order", "OrderItem")
        for model_name in models_running_store_event:
            model_class = self.get_model(model_name)
            post_save.connect(post_save_store_event, sender=model_class)
