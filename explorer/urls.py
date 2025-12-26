from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Index
    path("", views.index, name="index"),

    # Auth
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Profile
    path("profile/<str:username>/", views.profile_view, name="profile"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),

    # Games
    path("collatz/", views.collatz_game, name="collatz"),
    path("riemann/", views.riemann, name="riemann"),
    path("goldbach/", views.goldbach, name="goldbach"),
    path("goldbach/save-time/", views.goldbach_save_time, name="goldbach_save_time"),
    path("riemann-more/", views.riemannMore, name="riemann-more"),
    
    # Rankings
    path("ranking/", views.rankings, name="ranking"), # this is not working
]
