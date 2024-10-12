from django.urls import path
from accounts.views import UserView, LoginView

urlpatterns = [
    # Register a new user (POST)
    path('user/', UserView.as_view(), name="user_register"),
    
    # Get, update, and delete an existing user by ID (GET, PUT, PATCH, DELETE)
    path('user/<int:pk>/', UserView.as_view(), name="user_detail"),
    path('login/', LoginView.as_view(), name="user login"),
]
