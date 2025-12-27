from django.core.management.base import BaseCommand
from explorer.models import Achievement

class Command(BaseCommand):
    help = "Creates initial achievements"

    def handle(self, *args, **kwargs):
        achievements = [
            # Collatz
            {
                "name": "There is something about 73...",
                "description": "Reach 73 steps in collatz",
                "icon": "7️⃣3️⃣",
                "game_type": "collatz_steps",
                "threshold": 73,
                "comparison": "gte"
            },

            {
                "name": "Those aren't rookie numbers",
                "description": "Reach 100 steps in collatz",
                "icon": "💯",
                "game_type": "collatz_steps",
                "threshold": 100,
                "comparison": "gte"
            },

            {
                "name": "I got 200 problems and collatz is one of them...",
                "description": "Reach 200 steps in collatz",
                "icon": "🥇💯",
                "game_type": "collatz_steps",
                "threshold": 200,
                "comparison": "gte"
            },

            {
                "name": "Is not that big",
                "description": "Reach a max value of 500000 in Collatz",
                "icon": "🏢",
                "game_type": "collatz_max",
                "threshold": 500000,
                "comparison": "gte"
            },

            {
                "name": "Is over 9000000!",
                "description": "Reach a max value of 10000000 in Collatz",
                "icon": "🏔️",
                "game_type": "collatz_max",
                "threshold": 10000000,
                "comparison": "gte"
            },

            {
                "name": "To Infinity and Beyond",
                "description": "Reach a max value of 8000000000 in Collatz",
                "icon": "♾️",
                "game_type": "collatz_max",
                "threshold": 8000000000,
                "comparison": "gte"
            },

            # Goldbach
            {
                "name": "Ready, Set, Go!",
                "description": "Complete Goldbach game in under 120 seconds",
                "icon": "⏱️",
                "game_type": "goldbach_time",
                "threshold": 120,
                "comparison": "lte"
            },

            {
                "name": "Speed Runner",
                "description": "Complete Goldbach game in under 90 seconds",
                "icon": "🏃",
                "game_type": "goldbach_time",
                "threshold": 90,
                "comparison": "lte"
            },
        
            {
                "name": "Lightyear",
                "description": "Complete Goldbach game in under 60 seconds",
                "icon": "🐎",
                "game_type": "goldbach_time",
                "threshold": 60,
                "comparison": "lte"
            },

            {
                "name": "Prime Clairvoyance",
                "description": "Complete Goldbach game in under 35 seconds",
                "icon": "🤯",
                "game_type": "goldbach_time",
                "threshold": 35,
                "comparison": "lte"
            },
        ]

        for ach_data in achievements:
            achievement, created = Achievement.objects.get_or_create(
                name=ach_data["name"],
                defaults=ach_data
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {achievement.name}"))
            
            else: 
                self.stdout.write(f"Already exists: {achievement.name}")