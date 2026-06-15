from rest_framework.routers import DefaultRouter
from .views import QuoteViewSet, QuoteItemViewSet

router = DefaultRouter()
router.register(r"items", QuoteItemViewSet, basename="quoteitem")
router.register(r"", QuoteViewSet, basename="quote")

urlpatterns = router.urls
