from django.urls import path
from .views import login_view,registration_view,account,logout_view,user_ratings_create,user_ratings_delete

urlpatterns = [
    path('account/', account, name="account"),
    path('login/',login_view, name = "login"),
    path('register/',registration_view, name = 'register'),
    path('logout/', logout_view, name='logout'),
    path('user_ratings_create/<int:book_id>/', user_ratings_create, name='user_ratings_create'),
    path('user_ratings_delete/<int:book_id>/', user_ratings_delete, name='user_ratings_delete'),
]