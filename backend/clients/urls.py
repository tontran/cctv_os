from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, LeadViewSet, LocationViewSet, CCTVSystemViewSet

router = DefaultRouter()
router.register(r"", ClientViewSet, basename="client")
router.register(r"leads", LeadViewSet, basename="lead")
router.register(r"locations", LocationViewSet, basename="location")
router.register(r'systems', CCTVSystemViewSet, basename='cctvsystem')

urlpatterns = router.urls
