from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg


# Create your models here.

class Product(models.Model):
    _id = models.TextField()
    index = models.IntegerField(primary_key=True)
    url = models.TextField(max_length=100)
    name = models.CharField(max_length=100)
    sku = models.TextField(max_length=100)
    selling_price = models.FloatField()
    original_price = models.FloatField()
    currency = models.TextField()
    availability = models.CharField(max_length=50)
    color = models.TextField()
    category = models.CharField(max_length=100)
    source_website = models.TextField()
    breadcrumbs = models.TextField()
    description = models.TextField()
    brand = models.TextField()
    images = models.TextField()
    country = models.TextField()
    language = models.TextField()
    average_rating = models.FloatField()
    reviews_count = models.IntegerField()
    crawled_at = models.TextField()


class Comments(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    owner = models.CharField(max_length=50)
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        help_text='Рейтинг от 1 до 10'

    )


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_average_rating()
