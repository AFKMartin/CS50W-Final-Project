from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(max_length=400, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
@receiver(post_save, sender=User) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, "profile"):
        instance.profile.save()

class GameScore(models.Model):
    GAME_CHOICES = [
        ("collatz_steps", "Collatz Steps"),
        ("collatz_max", "Collatz Max Value"),
        ("goldbach_time", "Goldbach Time"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_type = models.CharField(max_length=20, choices=GAME_CHOICES)
    value = models.FloatField()  # steps, max value, or time
    created_at = models.DateTimeField(auto_now_add=True)

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=10)  # emoji I think, gotta test it
    game_type = models.CharField(max_length=20, choices=GameScore.GAME_CHOICES)
    threshold = models.FloatField()  # value needed to unlock
    comparison = models.CharField(
        max_length=10, 
        choices=[('gte', 'Greater than or equal'), ('lte', 'Less than or equal')],
        default='gte'
    )
    
    def __str__(self):
        return f"{self.icon} {self.name}"
    
    class Meta:
        ordering = ['game_type', 'threshold']


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'achievement')
        ordering = ['-unlocked_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"