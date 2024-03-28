from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from djongo import models


# Create your models here.

class Product(models.Model):
    _id = models.CharField(primary_key=True, max_length=255)
    index = models.IntegerField()
    url = models.TextField()
    name = models.TextField()
    sku = models.TextField()
    selling_price = models.IntegerField()
    currency = models.TextField()
    availability = models.BooleanField()
    color = models.TextField()
    category = models.TextField()
    source = models.TextField()
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

    def __str__(self):
        return self.name

    def update_average_rating(self):
        reviews = self.review_set.all()
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        self.average_rating = average_rating
        self.save()


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

class Purchases(models.Model):
    _id = models.CharField(primary_key=True, max_length=255)
    customer_id = models.IntegerField()
    product_count = models.IntegerField()
    product_price = models.IntegerField()
    date = models.DateTimeField()
    product_index = models.IntegerField()
    currency = models.TextField()
