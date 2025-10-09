from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import PaymentViewSet

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r"payments", PaymentViewSet, basename="payments")


urlpatterns = []

urlpatterns += router.urls
