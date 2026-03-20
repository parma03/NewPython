from rest_framework import serializers
from presentation.api.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'stock', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'stock', 'is_active')

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Harga tidak boleh negatif.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stok tidak boleh negatif.")
        return value
