from rest_framework.routers import DefaultRouter

from orders.views import v1 as views

app_name = "orders"


router = DefaultRouter()
router.register(r"history", views.EventViewSet)

urlpatterns = router.urls
