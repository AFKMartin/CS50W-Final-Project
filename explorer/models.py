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

