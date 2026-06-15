from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, LeadViewSet, LocationViewSet, CCTVSystemViewSet

router = DefaultRouter()
# Specific paths MUST come before empty root r''
# Otherwise r'' catches 'locations', 'leads', 'systems' as client PKs
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'systems', CCTVSystemViewSet, basename='cctvsystem')
router.register(r'', ClientViewSet, basename='client')

urlpatterns = router.urls
