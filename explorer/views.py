# explorer/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse
from .utils import *
from .models import *
from django.db.models import Max, Min
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

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

def riemannMore(request):
    return render(request, "explorer/riemann-more.html")

def goldbach(request):
    return render(request, "explorer/goldbach.html")

def ranking(request):
    return render(request, "explorer/ranking.html")

@csrf_exempt
def goldbach_save_time(request):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            time_value = float(request.POST.get("time"))

            # lower is better
            best_time = GameScore.objects.filter(
                user = request.user,
                game_type = "goldbach_time"
            ).aggregate(Min("value"))["value__min"]
            
            if best_time is None or time_value < best_time:
                GameScore.objects.create(
                    user = request.user,
                    game_type = "goldbach_time",
                    value = time_value
                )

            return JsonResponse({"status": "ok"})
        
        except (TypeError, ValueError):
            return JsonResponse({"status": "error"}, status = 400)
        
    return JsonResponse({"status": "forbidden"}, status= 403)

def collatz_game(request):
    res = None
    error = None
    if request.method == "POST":
        n_str = request.POST.get("number")

        if not n_str:
            error = "Please enter a number."
        else:
            try:
                n = int(n_str)  
                if n < 1 or n > 1000000:
                    error = "Please enter a number between 1 and 1.000.000" 
                else:
                    res = collatz_seq(n)  

                    if request.user.is_authenticated:
                        steps = res["steps"]
                        max_value = res["max_value"]

                        # Steps Record 
                        best_steps = GameScore.objects.filter(
                            user = request.user,
                            game_type = "collatz_steps"
                        ).aggregate(Max("value"))["value__max"]

                        if best_steps is None or steps > best_steps:
                            GameScore.objects.create(
                                user = request.user,
                                game_type = "collatz_steps",
                                value = steps
                            )
                        
                        # Value Record 
                        best_max = GameScore.objects.filter(
                            user = request.user,
                            game_type = "collatz_max"
                        ).aggregate(Max("value"))["value__max"]

                        if best_max is None or max_value > best_max:
                            GameScore.objects.create(
                                user = request.user,
                                game_type = "collatz_max",
                                value=max_value
                            )

            except ValueError:
                error = "Please enter a valid integer."

    return render(request, "explorer/collatz.html", {
        "result": res,
        "error": error
    })

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)

    # scores
    scores = GameScore.objects.filter(user=user)
    collatz_steps = scores.filter(game_type="collatz_steps").order_by("-value").first()
    collatz_max = scores.filter(game_type="collatz_max").order_by("-value").first()
    goldbach_time = scores.filter(game_type="goldbach_time").order_by("value").first()  # lower is better


    return render(request, "explorer/profile.html", {
        "profile_user": user,
        "profile": profile,
        "collatz_steps": collatz_steps,
        "collatz_max": collatz_max,
        "goldbach_time": goldbach_time,
    })