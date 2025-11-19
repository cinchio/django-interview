from django.urls import path
from .views import (
    PageListCreateView,
    PageRetrieveUpdateDestroyView,
    NavigationPagesView,
    MyPagesListView
)

app_name = 'pages'

urlpatterns = [
    path('', PageListCreateView.as_view(), name='page-list-create'),
    path('navigation/', NavigationPagesView.as_view(), name='navigation-pages'),
    path('my-pages/', MyPagesListView.as_view(), name='my-pages'),
    path('<slug:slug>/', PageRetrieveUpdateDestroyView.as_view(), name='page-detail'),
]
