from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    color = models.CharField(max_length=20, default="white")

    def __str__(self):
        return self.title
