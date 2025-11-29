from django.db import models
from django.utils import timezone

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=200)
    
    created_at = models.DateTimeField(auto_now_add=True)
    reminder_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
