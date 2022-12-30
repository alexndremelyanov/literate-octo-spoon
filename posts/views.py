from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from posts.models import Category, Comment, Post
from posts.permissions import IsAuthorOrReadOnly
from posts.serializers import (
    CategoryReadSerializer,
    CommentReadSerializer,
    CommentWriteSerializer,
    PostReadSerializer,
    PostWriteSerializer,
)


class BaseAPIListPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'size'
    max_page_size = 1000


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryReadSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = BaseAPIListPagination


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    pagination_class = BaseAPIListPagination

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return PostWriteSerializer

        return PostReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    pagination_class = BaseAPIListPagination

    def get_queryset(self):
        res = super().get_queryset()
        post_id = self.kwargs.get("post_id")
        return res.filter(post__id=post_id)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return CommentWriteSerializer

        return CommentReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()


class LikePostAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = BaseAPIListPagination

    def post(self, request, pk):
        user = request.user
        post = get_object_or_404(Post, pk=pk)

        if user in post.likes.all():
            post.likes.remove(user)

        else:
            post.likes.add(user)

        return Response(status=status.HTTP_200_OK)
