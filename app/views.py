from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
import random, os
from .models import OTPVerification, UserInfo
from django.conf import settings
from .utils.generate_qrs import generate_qr
from .utils.send_whatsapp_msg import send_interakt_button_message, send_interakt_message, INTERAKT_API_KEY

class OtpAuthViewSet(viewsets.ViewSet):

    def create(self, request):
        """
        Step 1: Generate OTP & send via WhatsApp
        """
        mobile = request.data.get("mobile")
        if not mobile:
            return Response({"success": False, "error": "Mobile number is required."}, status=400)

        otp = ''.join(random.choices('0123456789', k=6))

        # send OTP message
        send_interakt_button_message(
            api_key=INTERAKT_API_KEY,
            phone_number=mobile,
            template_name="otp_verification",
            language_code="en",
            body_values=[otp],
            button_values={"0": [otp]},
            callback_data="form_otp"
        )

        otp_obj = OTPVerification.objects.create(
            mobile=mobile,
            otp=otp,
            expires_at=timezone.now() + timedelta(minutes=5)
        )

        return Response({
            "success": True,
            "data": {"otp_id": otp_obj.id, "otp": otp},  # remove otp in prod
        })

    def update(self, request, pk):
        """
        Step 2: Verify OTP
        """
        otp_id = pk
        otp = request.data.get("otp")
        if not otp_id or not otp:
            return Response({"success": False, "error": "otp_id & otp required."}, status=400)

        try:
            otp_obj = OTPVerification.objects.get(id=otp_id)
        except OTPVerification.DoesNotExist:
            return Response({"success": False, "error": "Invalid OTP ID."}, status=404)

        if otp_obj.is_verified:
            return Response({"success": True, "data": {"otp_verified": True, "message": "OTP Already verified"}})

        if otp_obj.expires_at < timezone.now():
            return Response({"success": True, "data": {"otp_verified": False, "message": "OTP expired"}})

        if otp_obj.attempt_count > 2:
            return Response({"success": True, "data": {"otp_verified": False, "message": "OTP tried for more than 3 times"}})

        if otp_obj.otp != otp:
            otp_obj.attempt_count += 1
            otp_obj.save()
            return Response({"success": True, "data": {"otp_verified": False, "message": "Incorrect OTP. Please try again."}})

        otp_obj.is_verified = True
        otp_obj.save()

        return Response({"success": True, "data": {"otp_verified": True, "mobile": otp_obj.mobile}})

class FormSubmissionViewSet(viewsets.ViewSet):
    """
    Step 3: After OTP verified → store info → generate QR → send via WhatsApp
    """
    def create(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        mobile = request.data.get("mobile")

        if not all([name, mobile]):
            return Response({"success": False, "error": "Name & mobile are required."}, status=400)

        qr_folder = os.path.join(settings.MEDIA_ROOT, "qrs")
        qr_filename = f"{mobile}.png"
        qr_path = generate_qr(data=mobile, folder=qr_folder, filename=qr_filename)

        # Save info
        user, created = UserInfo.objects.get_or_create(
            mobile=mobile, defaults={"name": name, "email": email, "qr_image": f"qrs/{qr_filename}"}
        )

        # Send QR on WhatsApp
        media_url = f"{settings.MEDIA_URL}qrs/{qr_filename}"

        send_interakt_message(
            api_key=INTERAKT_API_KEY,
            phone_number=mobile,
            template_name="qr_code",
            language_code="en",
            body_values=[f"{name}"],
            header_values=[f"{request.build_absolute_uri(media_url)}"],
            callback_data="form_otp"
        )

        return Response({
            "success": True,
            "data": {"qr_url": media_url, "user_created": created}
        })

