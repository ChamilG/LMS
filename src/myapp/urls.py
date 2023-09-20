from django.urls import path
from .views import home,book_detail,increase_no_of_views, search_result, categories_view

urlpatterns = [
    path('',home, name='home' ),
    path('book/<int:book_id>/', book_detail, name='book_detail'),
    path('/<str:category>', categories_view, name='category'),
    path('increase_no_of_views/<int:book_id>/', increase_no_of_views, name='user_ratings_delete'),
    path('search/', search_result, name='search_result'),
]
