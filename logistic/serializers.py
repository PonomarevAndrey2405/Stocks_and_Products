from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)


    def create(self, validated_data):
        positions = validated_data.pop('positions')

        stock = super().create(validated_data)

        for elem in positions:
            new_stock_product = StockProduct.objects.create(product=elem['product'], stock=stock,
                                                            quantity=elem['quantity'], price=elem['price'])
            stock.positions.add(new_stock_product)

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')

        stock = super().update(instance, validated_data)

        for elem in positions:
            StockProduct.objects.update_or_create(defaults={'quantity': elem['quantity'], 'price': elem['price']},
                                                  product=elem['product'], stock=stock)

        return stock

    class Meta:
        model = Stock
        fields = ['address', 'positions']
