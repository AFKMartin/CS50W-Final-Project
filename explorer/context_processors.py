from .models import UserAchievement

def unread_achievements(request):
    
    if request.user.is_authenticated:
        count = UserAchievement.objects.filter(
            user=request.user,
            viewed=False
        ).count()
        return {"unread_achievements_count": count}
    return {"unread_achievements_count": 0}
