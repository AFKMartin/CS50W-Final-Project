# explorer/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse
from .utils import *

def index(request):
    return render(request, "explorer/index.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "explorer/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "explorer/register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        return redirect("index")
    else:
        return render(request, "explorer/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "explorer/login.html", {
                "message": "Invalid username or password."
            })
    return render(request, "explorer/login.html")

def logout_view(request):
    logout(request)
    return redirect("index")

def profile(request):
    return render(request, "explorer/profile.html")

def collatz(request):
    return render(request, "explorer/collatz.html")

def riemann(request):
    return render(request, "explorer/riemann.html")

def golbatch(request):
    return render(request, "explorer/golbatch.html")

def ranking(request):
    return render(request, "explorer/ranking.html")

def collatz_game(request):
    res = None
    error = None
    if request.method == "POST":
        try:
            n_str = request.POST.get("number")
            if not n_str:
                error = "Please enter a number."
            else:
                n = int(n_str)
                if n < 1 or n > 1000000:
                    error = "Please enter a number between 1 and 1.000.000"
                else:
                    res = collatz_seq(n)
        except ValueError:
            error = "Please enter a valid integer."

    return render(request, "explorer/collatz.html", {
        "result": res,
        "error": error
    })


