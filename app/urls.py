# app/urls.py
from rest_framework.routers import DefaultRouter
from .views import OtpAuthViewSet, FormSubmissionViewSet

router = DefaultRouter()
router.register(r'otp-api', OtpAuthViewSet, basename='otp-api')
router.register(r'form-submit', FormSubmissionViewSet, basename='form-submit')

urlpatterns = router.urls
