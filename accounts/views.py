from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accounts.models import User, UserDetail
from django.db.models import Q
import datetime as dt
import random as rd
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import ProfileSerializer, ProfileUpdateSerializer, ChangePasswordSerializer, LoginSerializer
from accounts.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from rest_framework.generics import UpdateAPIView


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]
    
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                response = {
                    'status': 'failed',
                    'message': 'Old password is incorrect'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.data.get('new_password'))
            user.save()
            response = {
                'status': 'success',
                'message': 'Password updated successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        
        response = {
            'status': 'failed',
            'message': 'Password update failed',
            'errors': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)



class ProfileViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return user profile with nested UserDetail if available."""
        serializer = ProfileSerializer(request.user)
        return Response(
            {
                "status": "success",
                "message": "User profile fetched successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        """Create or update UserDetail for the authenticated user."""
        user = request.user
        if user.org_admin:
            return Response({
                    "status": "failed",
                    "message": "College Admin Profile Cannot be Updated",
                    "data": ProfileSerializer(user).data,
                }, status=status.HTTP_403_FORBIDDEN)
        if user.user_detail:
            # Update existing detail
            serializer = ProfileUpdateSerializer(
                user.user_detail, data=request.data, partial=True
            )
        else:
            # Create new detail
            serializer = ProfileUpdateSerializer(data=request.data)

        if serializer.is_valid():
            detail = serializer.save()
            if not user.user_detail:
                # Link UserDetail with User
                user.user_detail = detail
                user.save()

            return Response(
                {
                    "status": "success",
                    "message": "Profile updated successfully",
                    "data": ProfileSerializer(user).data,
                },
                status=status.HTTP_202_ACCEPTED,
            )

        return Response(
            {
                "status": "failed",
                "message": "Invalid data",
                "errors": serializer.errors,
                "data": {},
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            res = {
                "status": "failed",
                "message": "Please provide both email and password",
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email.lower())
        except User.DoesNotExist:
            res = {"status": "failed", "message": "Account does not exist"}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            res = {"status": "failed", "message": "Invalid credentials"}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_verified:
            res = {"status": "failed", "message": "Please verify your email first"}
            return Response(res, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        user_data = LoginSerializer(user).data

        res = {
            "status": "success",
            "message": "User logged in successfully",
            "data": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": user_data,
            },
        }
        return Response(res, status=status.HTTP_200_OK)
