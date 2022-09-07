
from django.urls import path
from . import views
from .views import (
        PostListView, 
        PostDetailView,     
        PostCreateView,
        PostUpdateView,
        PostDeleteView,
        )




urlpatterns = [
# when we use a class, we cannot pass that directly in the url we need to convert that to a view, and as_view function does that
    path('', PostListView.as_view(), name = 'blog-home'),

# we will have to create a url patterns for post1, post2 etc, so we mention post/ primary key and data type of primary key i.e int
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name = 'post-delete'),
    path('about/', views.about, name = 'blog-about'),
]

