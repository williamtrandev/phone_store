from django.db import models
from applications.commons.utils import generate_unique_id_24char


class Customer(models.Model):
    id = models.CharField(default=generate_unique_id_24char, max_length=100, primary_key=True)
    username = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.fullname

    class Meta:
        db_table = 'customer'


class Product(models.Model):
    id = models.CharField(default=generate_unique_id_24char, max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE)
    is_phone = models.BooleanField(default=False)
    color = models.CharField(max_length=100, blank=True, null=True)
    ram = models.IntegerField(blank=True, null=True)
    rom = models.IntegerField(blank=True, null=True)
    price = models.IntegerField()
    retail_price = models.IntegerField()
    detail = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.is_phone:
            details = []
            if self.color:
                details.append(f"Color: {self.color}")
            if self.ram:
                details.append(f"RAM: {self.ram}GB")
            if self.rom:
                details.append(f"ROM: {self.rom}GB")
            return f"{self.name} ({', '.join(details)})"
        return self.name

    class Meta:
        db_table = 'product'


class Category(models.Model):
    id = models.CharField(default=generate_unique_id_24char, max_length=100, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'


class CartItem(models.Model):
    id = models.CharField(default=generate_unique_id_24char, max_length=100, primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def total_price(self):
        return self.product.retail_price * self.quantity

    class Meta:
        db_table = 'cart_item'


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
    ]
    id = models.CharField(default=generate_unique_id_24char, max_length=100, primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(default=0)

    class Meta:
        db_table = 'order'


class OrderItem(models.Model):
    id = models.CharField(default=generate_unique_id_24char, max_length=100, primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)

    class Meta:
        db_table = 'order_item'
