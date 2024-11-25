from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("accounts/login/", views.login_view, name="login"),  
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('profile/<str:username>/', views.profile, name='profile'),
    path("create_post", views.create_post, name="create_post"),
    path("following", views.following, name="following"),
    path('update_post/<int:post_id>/', views.update_post, name='update_post'),
    path('toggle_like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('accounts/', include('django.contrib.auth.urls')),  # Added this line
    path('index/', views.index, name='home'),  
]
