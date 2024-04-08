from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.loginPage, name="login"),
    path("register/", views.registerPage, name="register"),
    path("logout/", views.logoutUser, name="logout"),
    path("home/", views.home, name="home"),
    path("room/<str:pk>/", views.room, name="room"),
    path("create-room/", views.createRoom, name="create-room"),
    path("update-room/<str:pk>", views.updateRoom, name="update-room"),
    path("delete-room/<str:pk>", views.deleteRoom, name="delete-room"),
    path("delete-message/<int:room_id>/<int:pk>", views.deleteMessage, name="delete-message"),

]
