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
    path("profile/", views.profile, name="profile"),

    # Games
    path("collatz/", views.collatz, name="collatz"),
    path("riemann/", views.riemann, name="riemann"),
    path("golbatch/", views.golbatch, name="golbatch"),

    # Rankings
    path("ranking/", views.ranking, name="ranking"),
]
