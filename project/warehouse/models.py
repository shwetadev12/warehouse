from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    PROFILE_TYPES = [
        ('warehouses_owner', 'Warehouse owner'),
        ('warehouses_manager', 'Warehouses manager'),
        ('company_owner', 'Company owner')]
    profile_type = models.CharField(max_length=64, choices=PROFILE_TYPES)

    def __str__(self):
        return self.username

class WarehouseManager(models.Model):
    manager = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="manager_user"
    )
    warehouse = models.ForeignKey(
        "Warehouse", on_delete=models.CASCADE, related_name="warehouse_manager"
    )


class Company(models.Model):
    owner = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="company_user"
    )
    company_name = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    email = models.EmailField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.company_name


class Warehouse(models.Model):
    name = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    companies = models.ManyToManyField(Company)

    def __str__(self):
        return self.name


class Product(models.Model):
    company = models.ForeignKey(
        "Company", on_delete=models.CASCADE, related_name="product"
    )
    product_name = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product_name


class OrderProduct(models.Model):
    ORDER_STATUS = (('Add', 'add'), ('Deduct', 'deduct'))
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="order_products"
    )
    count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, choices=ORDER_STATUS, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_name

