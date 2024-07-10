from django.urls import path
from . import views
app_name = "discord"

urlpatterns = [
    # Main application URLs
    path('', views.home,  name="home"),                  # URL for home page
    path('room/<str:pk>/', views.room, name="room"),     # URL for individual room page
    path('profile/', views.userProfile, name="user-profile"),  # URL for user profile page
]