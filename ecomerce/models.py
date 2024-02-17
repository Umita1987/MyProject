from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg


# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.IntegerField()
    in_stock = models.BooleanField()
    average_rating = models.FloatField(default=0.0, editable=False)

    def __str__(self):
        return self.title

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





