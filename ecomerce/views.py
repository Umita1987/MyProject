from typing import Type

from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Product, Comments
from .premissions import IsUserOrReadOnly
from .serializers import ProductSerializer, UserSerializer, CommentsSerializer


class ProductViewsSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', "in_stock", "rating", "price"]


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)

    def create(self, request, *args, **kwargs):
        self.serializer_class = UserSerializer
        self.permission_classes = (AllowAny,)
        return super(UserViewSet, self).create(request, *args, **kwargs)


class CommentsViewsSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class: Type[CommentsSerializer] = CommentsSerializer
    permission_classes = [IsAuthenticated]


class ProductListViewsSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id', 'title']
