from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegisterViewsSet, LogoutView, ReviewViewsSet, \
    DeleteCommentsView, \
    ProductUpdateView, ProductDetailView, CommentsViewsSet, ProductAPIView, ProductViewsSet, \
    ProductDeleteView, PurchasesSeriesView

router = DefaultRouter()

router.register(r"products", ProductViewsSet, basename="products")
router.register(r'comments', CommentsViewsSet)
router.register('register', RegisterViewsSet)
router.register('review', ReviewViewsSet)
router.register(r"data", PurchasesSeriesView, basename="data")

urlpatterns = [
    path('', include(router.urls)),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('comments/<int:pk>/', DeleteCommentsView.as_view()),
    path('products/delete/<str:pk>/', ProductDeleteView.as_view(), name="delete"),
    path('products/update/<str:pk>/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<str:_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/', ProductAPIView.as_view(), name='product-list'),
    path('product/<str:_id>/', ProductAPIView.as_view(), name='product-detail'),


]
