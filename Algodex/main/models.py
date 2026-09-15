from django.db import models
from django.contrib.auth.models import User

CATEGORY = [
    ("F2L", "F2L"),
    ("OLL", "OLL"),
    ("PLL", "PLL")
]

class Algorithm(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=3, choices=CATEGORY)
    moves = models.CharField(max_length=255)
    description = models.TextField(default="")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    yes_count = models.IntegerField(default=0)
    no_count = models.IntegerField(default=0)
    voters = models.ManyToManyField(User, related_name="voters", blank=True)

    def __str__(self):
        return self.name


class Solve(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.FloatField()
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.time)