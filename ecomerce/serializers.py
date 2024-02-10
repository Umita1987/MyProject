from django.contrib.auth.models import User
from rest_framework import serializers

from MyProject.ecomerce.models import Product, Comments


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(request_data=validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance = super().update(instance, validated_data)
        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'category', 'quantity', 'price', 'rating', 'available']

    def create(self, validated_data):
        return Product.objects.create_user(request_data=validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.category = validated_data.get('category', instance.category)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.price = validated_data.get('price', instance.price)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.available = validated_data.get('available', instance.rating)
        instance = super().update(instance, validated_data)
        instance.save()
        return instance


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'title', 'text', 'owner']
        read_only_fields = ('owner',)

    def create(self, validated_data):
        user = self.context['request'].user
        return Comments.objects.create(owner=user, **validated_data)
