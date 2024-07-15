from django.urls import path
from . import views
app_name = "discord"

urlpatterns = [
    # Main application URLs
    path('', views.home,  name="home"),                  # URL for home page
    path('room/<str:pk>/', views.room, name="room"),     # URL for individual room page
    path('profile/', views.userProfile, name="user-profile"),  # URL for user profile page

    # Authentication URLs
    path('login/', views.loginPage, name="login"),       # URL for login page
    path('logout/', views.logoutUser, name="logout"),    # URL for logout page
    path('register/', views.registerPage, name="register"),  # URL for registration page

    # Room management URLs
    path('create-room/', views.createRoom, name="create-room"),  # URL for creating a new room

   # User profile management URL
    path('update-user/', views.updateUser, name="update-user"),  # URL for updating user profile

    # Other URLs
    path('topics/', views.topicsPage, name="topics"),    # URL for displaying topics
    path('activity/', views.activityPage, name="activity"),  # URL for displaying activity
]