from django.db import models
from applications.commons.utils import generate_unique_id_24char


class Staff(models.Model):
    id = models.CharField(default=generate_unique_id_24char, max_length=100, primary_key=True)
    username = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    class Meta:
        db_table = 'staff'


class Customer(models.Model):
    id = models.CharField(default=generate_unique_id_24char, max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    class Meta:
        db_table = 'customer'


