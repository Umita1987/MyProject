from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import ProductViewsSet, CommentsViewsSet, RegisterViewsSet, LogoutView, ReviewViewsSet

router = DefaultRouter()

router.register(r"product", ProductViewsSet)
router.register(r'comments', CommentsViewsSet)
router.register('register', RegisterViewsSet)
router.register('review', ReviewViewsSet)


urlpatterns = [
    path('', include(router.urls)),
    path('logout/', LogoutView.as_view(), name='auth_logout')
]
