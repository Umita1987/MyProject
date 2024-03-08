from typing import Type

import pymongo
from bson import ObjectId
from django.contrib.auth.models import User
from pymongo import MongoClient
from rest_framework import viewsets, status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Comments, Review, Product
from .paginations import PaginationList
from .premissions import IsOwnerOrReadOnly
from .serializers import ProductSerializer, CommentsSerializer, RegisterSerializer, MyTokenObtainPairSerializer, \
    ReviewSerializer, DeleteDocumentSerializer


class ProductViewsSet(viewsets.ViewSet):
    pagination_class = PaginationList

    def list(self, request):
        client = pymongo.MongoClient("mongodb://localhost:27017")
        db = client["clothes"]
        products_collection = db["brands"]
        products_data = products_collection.find()
        serializer = ProductSerializer(products_data, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product_data = serializer.validated_data
            client = pymongo.MongoClient("mongodb://localhost:27017")
            db = client["clothes"]
            products_collection = db["brands"]
            result = products_collection.insert_one(product_data)
            if result.inserted_id:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response("Failed to insert product into MongoDB", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["clothes"]
        products_collection = db["brands"]

        try:
            object_id = ObjectId(pk)
            product = products_collection.find_one({"_id": object_id})
            if product:
                serializer = ProductSerializer(product)
                return Response(serializer.data)
            else:
                return Response("Product not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response("Invalid ObjectId provided", status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["clothes"]
        products_collection = db["brands"]

        try:
            object_id = ObjectId(pk)
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                product_data = serializer.validated_data
                result = products_collection.update_one({"_id": object_id}, {"$set": product_data})
                if result.modified_count > 0:
                    updated_product = products_collection.find_one({"_id": object_id})
                    serializer = ProductSerializer(updated_product)
                    return Response(serializer.data)
                else:
                    return Response("Product not found", status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response("Invalid ObjectId provided", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["clothes"]
        products_collection = db["brands"]

        try:
            object_id = ObjectId(pk)
            result = products_collection.delete_one({"_id": object_id})
            if result.deleted_count > 0:
                return Response("Product deleted successfully", status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("Product not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response("Invalid ObjectId provided", status=status.HTTP_400_BAD_REQUEST)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class CommentsViewsSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class: Type[CommentsSerializer] = CommentsSerializer
    pagination_class = PaginationList
    # permission_classes = [IsAuthenticated]


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
    # permission_classes = (IsAuthenticated,)
    serializer_class = ReviewSerializer


class DeleteCommentsView(generics.DestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class DeleteDocumentView(APIView):
    def post(self, request):
        serializer = DeleteDocumentSerializer(data=request.data)
        if serializer.is_valid():
            document_id = serializer.validated_data['document_id']

            # Connect to your MongoDB
            client = MongoClient('localhost', 27017)
            db = client['clothes']
            collection = db['brands']

            # Delete the document
            result = collection.delete_one({'_id': document_id})
            if result.deleted_count == 1:
                return Response({'message': 'Document deleted successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(print("delete Product"))


class ProductUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    partial = True


class CustomProductViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["clothes"]
        products_collection = db["brands"]

        # Retrieve the product details based on the provided primary key (pk)
        product_data = products_collection.find_one({"_id": ObjectId(pk)})

        if product_data:
            serializer = ProductSerializer(product_data)  # Serialize the product data
            return Response(serializer.data)
        else:
            return Response("Product not found", status=404)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductAPIView(APIView):
    @staticmethod
    def get(request, _id=None):
        if _id is not None:
            try:
                product = Product.objects.get(_id=id)
                serializer = ProductSerializer(product)
                return Response(serializer.data)
            except Product.DoesNotExist:
                return Response("Product not found", status=status.HTTP_404_NOT_FOUND)
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Added Successfully", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, _id):
        try:
            product = Product.objects.get(_id=id)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("Updated Successfully")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response("Product not found", status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, _id):
        try:
            product = Product.objects.get(_id=id)
            product.delete()
            return Response("Deleted Successfully", status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response("Product not found", status=status.HTTP_404_NOT_FOUND)
