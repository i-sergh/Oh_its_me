from django.urls import path
from . import views

urlpatterns = [
    path('' ,views.face_site , name='me'),
    path('blog/login/', views.login_user, name="login"),
    path('blog/logout/', views.logout_user, name="logout"),
    path('blog/register/', views.register_user, name="register"),

    path('blog/', views.home, name='home'),
    path('blog/room/<str:pk>/', views.room, name='room'),
    path('blog/random/', views.random_room, name='random'),
    
    path('blog/profile/<str:pk>', views.user_profile, name='user-profile'),
    
    path('blog/create-room/', views.create_room, name='create-room'),
    path('blog/update-room/<str:pk>', views.update_room, name='update-room'),
    path('blog/delete-room/<str:pk>', views.delete_room, name='delete-room'),
    path('blog/delete-comment/<str:pk>', views.delete_comment, name='delete-comment'),

    
]

