from rest_framework.routers import DefaultRouter
from financial.views import (
    ContractDataViewSet, BillingPolicyViewSet, InvoiceConfigViewSet, FeeBillingViewSet, FeeDetailsViewSet
)


router = DefaultRouter()
router.register(r"contract-data", ContractDataViewSet)
router.register(r"billing-policy", BillingPolicyViewSet)
router.register(r"invoice-config", InvoiceConfigViewSet)
router.register(r"fee-billing", FeeBillingViewSet)
router.register(r"fee-details", FeeDetailsViewSet)

urlpatterns = router.urls
