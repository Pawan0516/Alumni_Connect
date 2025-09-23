from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from organization.models import College, User
from organization.serializers import CollegeSerializer, OnboardSerializer, CollegeCreateSerializer
import datetime as dt
import random as rd
from emails.utils import send_admin_onboarding_otp


class OnboardCollegeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OnboardSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            email = data.get("email").lower()
            password = data.get("password")
            try:
                # Check if user exists
                if User.objects.get(email=email):
                    res = {
                        "status": "failed",
                        "message": "Account already exists",
                        "data": {"email": email},
                    }
                    return Response(res, status=status.HTTP_409_CONFLICT)

            except User.DoesNotExist:
                # Create college_admin
                college_admin = User.objects.create_user(email=email, password=password, org_admin=True)

                # Generate OTP
                otp = str(rd.randint(100000, 999999))
                college_admin.email_otp = otp
                college_admin.email_otp_ts = dt.datetime.now()
                college_admin.save()

                # Send OTP via Email
                send_admin_onboarding_otp(email, otp)


                res = {
                    "status": "success",
                    "message": "College Admin registered. Please verify your email.",
                    "data": {"userId": college_admin.id, "email": college_admin.email},
                }
                return Response(res, status=status.HTTP_201_CREATED)

        res = {
            "status": "failed",
            "message": "Account registration failed",
            "errors": serializer.errors,
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)


class EmailVerifyViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            res = {
                "status": "failed",
                "message": "Email and OTP are required",
                "data": {},
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email.lower())
        except User.DoesNotExist:
            res = {
                "status": "failed",
                "message": "Account not found",
                "data": {},
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        if user.email_otp != otp:
            res = {"status": "failed", "message": "Invalid OTP", "data": {}}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        # Mark verified
        user.is_verified = True
        user.email_verified_at = dt.datetime.now()
        user.email_otp = None
        user.save()

        res = {
                "status": "success", 
                "message": "Email verified. Onboard Your College.", 
                "data": {"userId": user.id}
               }
        return Response(res, status=status.HTTP_200_OK)


class CollegeAPIView(APIView):
    authentication_classes = []  # No authentication
    permission_classes = []      # Open to all

    def post(self, request):
        serializer = CollegeCreateSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.pop("email")

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"status": "failed", "message": "User with this email does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if user is org_admin and verified
            if not (user.org_admin and getattr(user, "is_verified", False)):
                return Response(
                    {"status": "failed", "message": "You are not allowed to add a college."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Check if this user already linked to a college
            if College.objects.filter(admin=user, is_deleted=False).exists():
                return Response(
                    {"status": "failed", "message": "This email is already linked to a college."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create the college
            college = College.objects.create(admin=user, **serializer.validated_data)

            return Response(
                {
                    "status": "success",
                    "message": "College created successfully and is pending approval.",
                    "college": CollegeSerializer(college).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CollegeDetailAPIView(APIView):
    """
    GET: Anyone can fetch a college by handle (with social URLs).
    PUT/PATCH: Only the admin of the college can update it.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, handle, *args, **kwargs):
        try:
            college = College.objects.get(handle=handle)
        except College.DoesNotExist:
            res = {
                    "status": "failed", 
                    "message": "College not found",
                    "data": {}
                }
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        serializer = CollegeSerializer(college)
        res = {
                "status": "success",
                "message": "College details fetched successfully",
                "data": serializer.data,
            }
        return Response(res, status=status.HTTP_200_OK)

    def patch(self, request, handle, *args, **kwargs):
        try:
            college = College.objects.get(handle=handle)
        except College.DoesNotExist:
            res = {
                    "status": "failed", 
                    "message": "College not found",
                    "data": {}
                }
            return Response(res, status=status.HTTP_404_NOT_FOUND)


        # Only admin can modify
        if college.admin != request.user:
            res = {
                    "status": "failed",
                    "message": "Only college admin can modify details",
                    "data": {},
                }
            return Response(res, status=status.HTTP_403_FORBIDDEN)

        serializer = CollegeSerializer(college, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            res = {
                    "status": "success",
                    "message": "College details updated successfully",
                    "data": serializer.data,
                }
            return Response(res, status=status.HTTP_200_OK)
        
        res = {
                "status": "failed",
                "message": "Invalid data",
                "data": serializer.errors,
            }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
