"""
Presentation Layer - Products API Views
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from presentation.api.products.models import Product
from presentation.api.products.serializers import ProductSerializer, ProductCreateUpdateSerializer


class IsAdminRole:
    @staticmethod
    def check(user):
        return user.is_authenticated and user.role == 'admin'


class ProductListCreateView(APIView):
    """GET /api/v1/products/ - Semua user bisa lihat
       POST /api/v1/products/ - Hanya admin"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search = request.query_params.get('search', '')
        if search:
            products = Product.objects.filter(name__icontains=search) | \
                       Product.objects.filter(description__icontains=search)
            products = products.distinct().order_by('-created_at')
        else:
            products = Product.objects.all().order_by('-created_at')

        serializer = ProductSerializer(products, many=True)
        return Response({"data": serializer.data, "total": products.count()})

    def post(self, request):
        if not IsAdminRole.check(request.user):
            return Response({"message": "Akses ditolak. Hanya admin."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProductCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response({
                "message": "Produk berhasil ditambahkan.",
                "data": ProductSerializer(product).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    """GET, PUT, DELETE /api/v1/products/<id>/"""
    permission_classes = [IsAuthenticated]

    def _get_product(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self._get_product(pk)
        if not product:
            return Response({"message": "Produk tidak ditemukan."}, status=status.HTTP_404_NOT_FOUND)
        return Response(ProductSerializer(product).data)

    def put(self, request, pk):
        if not IsAdminRole.check(request.user):
            return Response({"message": "Akses ditolak."}, status=status.HTTP_403_FORBIDDEN)

        product = self._get_product(pk)
        if not product:
            return Response({"message": "Produk tidak ditemukan."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductCreateUpdateSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            product = serializer.save()
            return Response({
                "message": "Produk berhasil diperbarui.",
                "data": ProductSerializer(product).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not IsAdminRole.check(request.user):
            return Response({"message": "Akses ditolak."}, status=status.HTTP_403_FORBIDDEN)

        product = self._get_product(pk)
        if not product:
            return Response({"message": "Produk tidak ditemukan."}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response({"message": "Produk berhasil dihapus."}, status=status.HTTP_200_OK)
