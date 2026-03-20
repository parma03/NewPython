"""
Presentation Layer - Auth API Views
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model

from presentation.api.auth.serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer
from application.services.analytics_service import AnalyticsService
from infrastructure.repositories.user_repository import DjangoUserRepository
from infrastructure.repositories.product_repository import DjangoProductRepository
from django.utils import timezone

User = get_user_model()


class RegisterView(APIView):
    """POST /api/v1/auth/register/"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Registrasi berhasil.",
                "user": UserProfileSerializer(user).data,
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """POST /api/v1/auth/login/"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response(
                {"message": "Username atau password salah."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {"message": "Akun tidak aktif."},
                status=status.HTTP_403_FORBIDDEN
            )

        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login berhasil.",
            "user": UserProfileSerializer(user).data,
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """POST /api/v1/auth/logout/"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout berhasil."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"message": "Token tidak valid."}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """GET /api/v1/auth/profile/"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserProfileSerializer(request.user).data)


class DashboardStatsView(APIView):
    """GET /api/v1/auth/dashboard-stats/"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_repo = DjangoUserRepository()
        product_repo = DjangoProductRepository()
        analytics = AnalyticsService(user_repo, product_repo)

        if request.user.role == 'admin':
            stats = analytics.get_dashboard_stats()
        else:
            stats = analytics.get_user_stats()

        return Response(stats)
