from django.urls import path
from .views import (
    PostListCreateView,
    PostRetrieveUpdateDestroyView,
    MyPostsListView
)

app_name = 'posts'

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('my-posts/', MyPostsListView.as_view(), name='my-posts'),
    path('<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
]
