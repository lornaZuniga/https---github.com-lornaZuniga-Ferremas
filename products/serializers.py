from rest_framework import serializers
from .models import Product, Price, InventoryMovement, Category

class PriceSerializer(serializers.ModelSerializer):
    Valor = serializers.DecimalField(source='value', max_digits=10, decimal_places=2)

    class Meta:
        model = Price
        fields = ['Valor']

    def validate_Valor(self, value):
        if value <= 0:
            raise serializers.ValidationError("El valor del precio debe ser positivo.")
        return value

class InventoryMovementSerializer(serializers.ModelSerializer):
    movement_type_display = serializers.CharField(source='get_movement_type_display', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True) 

    class Meta:
        model = InventoryMovement
        fields = [
            'id', 'product', 'product_name', 'date', 'movement_type',
            'movement_type_display', 'quantity', 'description'
        ]
        read_only_fields = ['date', 'movement_type_display', 'product_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    Código_del_producto = serializers.CharField(source='code')
    Marca = serializers.CharField(source='brand')
    Código = serializers.CharField(source='brand_code')
    Nombre = serializers.CharField(source='name')
    Precio = PriceSerializer(many=True, source='prices', read_only=True)
    quantity = serializers.IntegerField(read_only=True)  # stock actual
    image_url = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    categoria_id = serializers.PrimaryKeyRelatedField(
        source='category', queryset=Category.objects.all(), required=False, allow_null=True
    )
    categoria_nombre = serializers.CharField(
        source='category.name', read_only=True, default=''
    )

    class Meta:
        model = Product
        fields = [
            'id', 'Código_del_producto', 'Marca', 'Código', 'Nombre',
            'Precio', 'quantity', 'categoria_id', 'categoria_nombre', 'image_url'
        ]

    def validate_Código_del_producto(self, value):
        # En update permitir el mismo código sin error
        product_id = self.instance.id if self.instance else None
        if Product.objects.exclude(id=product_id).filter(code=value).exists():
            raise serializers.ValidationError("El código del producto ya existe.")
        return value

    def create(self, validated_data):
        precios_data = self.initial_data.get('Precio', [])
        category = validated_data.pop('category', None)
        image_url = validated_data.pop('image_url', None)
        if not image_url:
            image_url = validated_data.get('image_url', None)
            
        product = Product.objects.create(
            code=validated_data.get('code'),
            brand=validated_data.get('brand'),
            brand_code=validated_data.get('brand_code'),
            name=validated_data.get('name'),
            category=category,
            image_url=image_url
        )
        for precio_data in precios_data:
            Price.objects.create(product=product, value=precio_data['Valor'])
        return product

    def update(self, instance, validated_data):
        precios_data = self.initial_data.get('Precio', [])
        category = validated_data.pop('category', None)
        instance.code = validated_data.get('code', instance.code)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.brand_code = validated_data.get('brand_code', instance.brand_code)
        instance.name = validated_data.get('name', instance.name)
        instance.category = category if category is not None else instance.category
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.save()

        # Actualizar precios
        instance.prices.all().delete()
        for precio_data in precios_data:
            Price.objects.create(product=instance, value=precio_data['Valor'])
        return instance
