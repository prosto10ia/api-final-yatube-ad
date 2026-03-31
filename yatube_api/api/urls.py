from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CommentViewSet,
    FollowViewSet,
    GroupViewSet,
    PostViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'users', UserViewSet, basename='users')
router.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'posts/<int:post_id>/comments/',
        CommentViewSet.as_view({
            'get': 'list',
            'post': 'create'
        })
    ),
    path(
        'posts/<int:post_id>/comments/<int:pk>/',
        CommentViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        })
    ),
]