from rest_framework.routers import DefaultRouter
from .views import QuoteViewSet, QuoteItemViewSet

router = DefaultRouter()
router.register(r"", QuoteViewSet, basename="quote")
router.register(r"items", QuoteItemViewSet, basename="quoteitem")

urlpatterns = router.urls
