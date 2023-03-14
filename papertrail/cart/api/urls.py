from rest_framework import routers

from .views import CartViewSet, CartItemViewSet

router = routers.SimpleRouter()
router.register(r'cart', CartViewSet)
router.register(r'cart-item', CartItemViewSet)

urlpatterns = router.urls
