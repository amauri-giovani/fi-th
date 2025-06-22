from rest_framework.routers import DefaultRouter
from companies.views import (
    GroupViewSet, CompanyViewSet, VipViewSet, CompanyContactViewSet, FeeDispatchContactViewSet, PointOfSaleViewSet
)


router = DefaultRouter()
router.register(r"groups", GroupViewSet)
router.register(r"companies", CompanyViewSet)
router.register(r"vips", VipViewSet)
router.register(r"company-contacts", CompanyContactViewSet)
router.register(r"fee-dispatch-contacts", FeeDispatchContactViewSet)
router.register(r"point-of-sale", PointOfSaleViewSet)

urlpatterns = router.urls
