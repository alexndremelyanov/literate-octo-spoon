from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/user/", include("users.urls", namespace="users")),
    path("api/posts/", include("posts.urls", namespace="posts")),
]
