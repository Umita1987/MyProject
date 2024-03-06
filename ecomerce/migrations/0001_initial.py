# Generated by Django 5.0.2 on 2024-03-06 17:04

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('_id', models.TextField()),
                ('index', models.IntegerField(primary_key=True, serialize=False)),
                ('url', models.TextField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('sku', models.TextField(max_length=100)),
                ('selling_price', models.FloatField()),
                ('original_price', models.FloatField()),
                ('currency', models.TextField()),
                ('availability', models.CharField(max_length=50)),
                ('color', models.TextField()),
                ('category', models.CharField(max_length=100)),
                ('source_website', models.TextField()),
                ('breadcrumbs', models.TextField()),
                ('description', models.TextField()),
                ('brand', models.TextField()),
                ('images', models.TextField()),
                ('country', models.TextField()),
                ('language', models.TextField()),
                ('average_rating', models.FloatField()),
                ('reviews_count', models.IntegerField()),
                ('crawled_at', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('owner', models.CharField(max_length=50)),
                ('rating', models.IntegerField(help_text='Рейтинг от 1 до 10', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='ecomerce.product')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomerce.product')),
            ],
        ),
    ]