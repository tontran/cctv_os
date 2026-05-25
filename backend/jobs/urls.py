from rest_framework.routers import DefaultRouter
from .views import JobViewSet, JobPhotoViewSet

router = DefaultRouter()
router.register(r"", JobViewSet, basename="job")
router.register(r"photos", JobPhotoViewSet, basename="jobphoto")

urlpatterns = router.urls
