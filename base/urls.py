from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),

    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('random/', views.random_room, name='random'),
    
    path('profile/<str:pk>', views.user_profile, name='user-profile'),
    
    path('create-room/', views.create_room, name='create-room'),
    path('update-room/<str:pk>', views.update_room, name='update-room'),
    path('delete-room/<str:pk>', views.delete_room, name='delete-room'),
    path('delete-comment/<str:pk>', views.delete_comment, name='delete-comment'),

]

