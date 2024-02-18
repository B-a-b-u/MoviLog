from django.urls import path
from .import views
urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("posts/<int:pk>", views.individual_post, name="individual_post"),
    path("delete_post/<int:pk>", views.delete_post, name="delete_post"),
    path("update_post/<int:pk>", views.update_post, name="update_post"),
    path("add_post/", views.add_post, name="add_post"),
    path("like_post/<int:pk>/", views.like_post, name="like_post"),  # New URL pattern for liking a post
    path("add_comment/<int:pk>/", views.add_comment, name="add_comment"),  # New URL pattern for adding 
   path("update_comment/<int:pk>/", views.update_comment, name="update_comment"),
   path("delete_comment/<int:pk>/", views.delete_comment, name="delete_comment"),


]