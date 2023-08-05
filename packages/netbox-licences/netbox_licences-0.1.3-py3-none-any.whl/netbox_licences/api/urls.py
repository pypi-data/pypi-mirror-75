from rest_framework import routers
from .views import SoftwareViewSet, LicenceViewSet

router = routers.DefaultRouter()
router.register('software', SoftwareViewSet)
# router.register('licences', LicenceViewSet)


urlpatterns = router.urls
