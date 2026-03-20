"""
Presentation Layer - Users API Views
Hanya admin yang dapat akses endpoint ini.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from presentation.api.users.serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer

User = get_user_model()


class IsAdminRole:
    """Custom permission check for admin role."""

    @staticmethod
    def check(user):
        return user.is_authenticated and user.role == 'admin'


class UserListCreateView(APIView):
    """GET, POST /api/v1/users/"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not IsAdminRole.check(request.user):
            return Response({"message": "Akses ditolak. Hanya admin."}, status=status.HTTP_403_FORBIDDEN)

        users = User.objects.all().order_by('-created_at')
        serializer = UserSerializer(users, many=True)
        return Response({"data": serializer.data, "total": users.count()})

    def post(self, request):
        if not IsAdminRole.check(request.user):
            return Response({"message": "Akses ditolak. Hanya admin."}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User berhasil dibuat.",
                "data": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """GET, PUT, DELETE /api/v1/users/<id>/"""
    permission_classes = [IsAuthenticated]

    def _get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        if not IsAdminRole.check(request.user):
            return Response({"message": "Akses ditolak."}, status=status.HTTP_403_FORBIDDEN)

        user = self._get_user(pk)
        if not user:
            return Response({"message": "User tidak ditemukan."}, status=status.HTTP_404_NOT_FOUND)

        return Response(UserSerializer(user).data)

    def put(self, request, pk):
        if not IsAdminRole.check(request.user):
            return Response({"message": "Akses ditolak."}, status=status.HTTP_403_FORBIDDEN)

        user = self._get_user(pk)
        if not user:
            return Response({"message": "User tidak ditemukan."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User berhasil diperbarui.",
                "data": UserSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not IsAdminRole.check(request.user):
            return Response({"message": "Akses ditolak."}, status=status.HTTP_403_FORBIDDEN)

        if str(request.user.id) == str(pk):
            return Response({"message": "Tidak bisa menghapus akun sendiri."}, status=status.HTTP_400_BAD_REQUEST)

        user = self._get_user(pk)
        if not user:
            return Response({"message": "User tidak ditemukan."}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"message": "User berhasil dihapus."}, status=status.HTTP_200_OK)
