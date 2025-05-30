from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    code = models.CharField(max_length=20, unique=True)
    brand = models.CharField(max_length=100)
    brand_code = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=0)  # Stock disponible
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    image_url = models.URLField(max_length=500, blank=True, null=True)  # Nuevo campo

    def __str__(self):
        return f"{self.code} - {self.name}"

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    date = models.DateTimeField(auto_now_add=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.code} - {self.value} ({self.date})"

class InventoryMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = (
        ('IN', 'Entrada'),
        ('OUT', 'Salida'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    date = models.DateTimeField(auto_now_add=True)
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Actualizar stock solo al crear un movimiento nuevo
        if not self.pk:
            if self.movement_type == 'IN':
                self.product.quantity += self.quantity
            else:  # 'OUT'
                if self.product.quantity < self.quantity:
                    raise ValueError("No hay suficiente stock para esta salida")
                self.product.quantity -= self.quantity
            self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.code} - {self.get_movement_type_display()} - {self.quantity} unidades"