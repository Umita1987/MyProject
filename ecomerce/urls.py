from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductViewsSet, CommentsViewsSet, RegisterViewsSet, LogoutView, ReviewViewsSet, DeleteCommentsView, \
    DeleteDocumentView

router = DefaultRouter()

router.register(r"products", ProductViewsSet, basename="products")
router.register(r'comments', CommentsViewsSet)
router.register('register', RegisterViewsSet)
router.register('review', ReviewViewsSet)

urlpatterns = [
    path('', include(router.urls)),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('comments/<int:pk>', DeleteCommentsView.as_view()),
    path('products/delete/<int:pk>', DeleteDocumentView.as_view(),name="delete")
]
