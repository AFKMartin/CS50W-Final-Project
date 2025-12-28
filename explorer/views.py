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
from django.contrib.auth.decorators import login_required

# Achivements unlocker helper
def achievements_helper(user, game_type, value):
    # Checks if user unlocked achievements
    achievements = Achievement.objects.filter(game_type=game_type)

    for achievement in achievements:
        # check if user alredy has the achievement
        already_unlocked = UserAchievement.objects.filter(
            user=user,
            achievement=achievement
        ).exists()
        
        if already_unlocked:
            continue

        # check if threshold is met
        unlocked = False
        if achievement.comparison == "gte" and value >= achievement.threshold:
            unlocked = True
        elif achievement.comparison == 'lte' and value <= achievement.threshold:
            unlocked = True
        
        if unlocked:
            UserAchievement.objects.create(user=user, achievement=achievement)

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

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)

    # scores
    scores = GameScore.objects.filter(user=user)
    collatz_steps = scores.filter(game_type="collatz_steps").order_by("-value").first()
    collatz_max = scores.filter(game_type="collatz_max").order_by("-value").first()
    goldbach_time = scores.filter(game_type="goldbach_time").order_by("value").first()  # lower is better

    # calculate rankings
    # collatz steps
    if collatz_steps:
        steps_rank = (
            GameScore.objects
            .filter(game_type = "collatz_steps")
            .values("user")
            .annotate(best_score = Max("value"))
            .filter(best_score__gt = collatz_steps.value)
            .count() + 1
        )
    else:
        steps_rank = None
    
    # collatz max value
    if collatz_max:
        max_rank = (
            GameScore.objects
            .filter(game_type = "collatz_max")
            .values("user")
            .annotate(best_score = Max("value"))
            .filter(best_score__gt = collatz_max.value)
            .count() + 1
        )
    else:
        max_rank = None

    # Goldbach time
    if goldbach_time:
        time_rank = (
            GameScore.objects
            .filter(game_type = "goldbach_time")
            .values("user")
            .annotate(best_score = Min("value"))
            .filter(best_score__lt = goldbach_time.value)
            .count() + 1
        )
    else:
        time_rank = None
    
    user_achievements = UserAchievement.objects.filter(user=user).select_related('achievement')

    return render(request, "explorer/profile.html", {
        "profile_user": user,
        "profile": profile,
        "collatz_steps": collatz_steps,
        "collatz_max": collatz_max,
        "goldbach_time": goldbach_time,
        "steps_rank": steps_rank,
        "max_rank": max_rank,
        "time_rank": time_rank,
        "user_achievements": user_achievements,
    })

@login_required
def edit_profile(request):
    if request.method == "POST":
        bio = request.POST.get("bio", "").strip()
        profile, created = Profile.objects.get_or_create(user = request.user)
        profile.bio = bio[:400]  # Limit to 400 characters
        avatar = request.FILES.get("avatar")

        if avatar:
            profile.avatar = avatar
    
        profile.save()
        return redirect("profile", username = request.user.username)
    
    return redirect("profile", username = request.user.username)

def collatz(request):
    return render(request, "explorer/collatz.html")

def riemann(request):
    return render(request, "explorer/riemann.html")

def riemannMore(request):
    return render(request, "explorer/riemann-more.html")

def goldbach(request):
    return render(request, "explorer/goldbach.html")

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

                # Achievements 
                achievements_helper(request.user, "goldbach_time", time_value)

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

                            # Achievements
                            achievements_helper(request.user, "collatz_steps", steps)
                        
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

                            # Achievemetns
                            achievements_helper(request.user, "collatz_max", max_value)

            except ValueError:
                error = "Please enter a valid integer."

    return render(request, "explorer/collatz.html", {
        "result": res,
        "error": error
    })

def rankings(request):
    # Collatz Steps
    top_steps = (
        User.objects
        .filter(gamescore__game_type = "collatz_steps")
        .annotate(best_steps = Max("gamescore__value"))
        .order_by("-best_steps")[:3]
    )

    # Collatz Max Value
    top_max_value = (
        User.objects
        .filter(gamescore__game_type = "collatz_max")
        .annotate(best_max = Max("gamescore__value"))
        .order_by("-best_max")[:3]
    )

    # Goldbach Best Time 
    top_goldbach = (
        User.objects
        .filter(gamescore__game_type = "goldbach_time")
        .annotate(best_time = Min("gamescore__value"))
        .order_by("best_time")[:3]
    )

    return render(request, "explorer/ranking.html", {
        "top_steps": top_steps,
        "top_max_value": top_max_value,
        "top_goldbach": top_goldbach,
    })
