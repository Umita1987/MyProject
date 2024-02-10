from django.db import models


# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField
    price = models.IntegerField
    rating = models.IntegerField
    in_stock = models.BooleanField


class Comments(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
