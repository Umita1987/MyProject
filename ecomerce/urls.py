from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductViewsSet, UserViewsSet

router = DefaultRouter()

router.register(r"product", ProductViewsSet)
router.register(r"user", UserViewsSet)

urlpatterns = [
    path('', include(router.urls))
]
