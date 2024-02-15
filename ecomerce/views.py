from typing import Type

from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Product, Comments, Review
from .paginations import PaginationList
from .serializers import ProductSerializer, CommentsSerializer, RegisterSerializer, MyTokenObtainPairSerializer, \
    ReviewSerializer


class ProductViewsSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    pagination_class = PaginationList
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', "in_stock", "price"]


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class CommentsViewsSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class: Type[CommentsSerializer] = CommentsSerializer
    pagination_class = PaginationList
    # permission_classes = [IsAuthenticated]


class ProductListViewsSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id', 'title']


class RegisterViewsSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ReviewViewsSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ReviewSerializer