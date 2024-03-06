from typing import Type

from bson import ObjectId
from pymongo import MongoClient
from rest_framework.decorators import api_view
import pymongo
from django.contrib.auth.models import User
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

    @staticmethod
    def delete(request, pk=None):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["ecommerce_db"]
        products_collection = db["products"]

        # Delete the product from MongoDB based on the provided primary key (pk)
        result = products_collection.delete_one({"_id": ObjectId(pk)})

        if result.deleted_count > 0:
            return Response("Product deleted successfully", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Product not found or failed to delete", status=status.HTTP_404_NOT_FOUND)





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

            #Connect to your MongoDB
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

