from django.urls import path
from . import views
app_name = "discord"

urlpatterns = [
    # Main application URLs
    path('', views.home,  name="home"),                  # URL for home page
    path('room/<str:pk>/', views.room, name="room"),     # URL for individual room page
   # path('profile/', views.userProfile, name="user-profile"),  # URL for user profile page

   # User profile management URL
    path('update-user/', views.updateUser, name="update-user"),  # URL for updating user profile

    # Other URLs
    path('topics/', views.topicsPage, name="topics"),    # URL for displaying topics
    path('activity/', views.activityPage, name="activity"),  # URL for displaying activity
]